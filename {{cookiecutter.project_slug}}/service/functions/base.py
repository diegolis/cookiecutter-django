

class BaseFunction():

    input_events = {
        'event_name': dict
    }
    output_events = {
        'event_name': dict
    }
    debug = False
    messages = 5

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.sync = os.getenv("PUBSUB_EMULATOR_HOST", "") != ""

    def subscription_name(self):
        return 'projects/{}/subscriptions/{}'.format(
            os.getenv("GOOGLE_PROJECT"), self.input)

    def valid_input(self, input):
        # REDEFINE THIS
        return True

    def get_pending_query(self):
        pending_query = ~Nested(
            path='filters',
            query=Match(filters__filter=self.filter_name())
        )
        return self.get_must_process_query() & pending_query

    def get_must_process_query(self):
        return MatchAll()

    def call(self, input):
        raise NotImplementedError

    def function_name(self):
        return type(self).__name__

    def callback(self, input_message):
        self.start_time = datetime.now()
        input = parse_message(input_message)
        self.status = ''
        # data['input'] = input_cast(input)
        if input is None:
            self.logger.debug("Received None message")
            self.status = 'None Input'
        elif not self.valid_input(input):
            self.logger.debug("Received invalid message: {}".format(input))
            self.status = 'Invalid Input'
        else:
            must_process = True
            if self.input_type is not dict:
                self.logger.debug('Looking {}'.format(input['id']))
                try:
                    instance = self.input_type.get(input['id'])
                except NotFoundError:
                    self.logger.debug('Instance not founded')
                    self.status = 'Not Found'
                    must_process = False
                if must_process and not input.get('force', False) and \
                        instance.last_filter_pass(self.filter_name()) \
                        is not None:
                    self.logger.debug('Instance already processed')
                    self.status = 'Duplicate input'
                    must_process = False
            else:
                instance = input
            if must_process:
                self.process(instance)

        if not self.sync:
            input_message.ack()

    def process(self, instance):
        self.start_time = datetime.now()
        self.logger.debug('Valid message {}'.format(instance))
        self.output_len = 0
        try:
            outputs = list(self.filter(instance) or [])
            self.status = 'Success'
        except Exception as e:
            self.logger.error(e)
            self.status = 'Failed'
            outputs = []
        for channel, message in outputs:
            self.logger.debug('Processed')
            if isinstance(message, dict):
                to_send = message
            else:
                to_send = message.to_message()
            try:
                pubsub.publish_message(channel, to_send)
                self.output_len += 1
            except Exception:
                self.status = 'Failed'
                pass
        self.logger.debug('Published')
        if self.input_type is not dict:
            instance = self.input_type.get(instance.meta.id)
            instance.add_filter_pass(self.filter_name())
        self.log_metric()

    def log_metric(self):
        end = datetime.now()

        metric = Log(
            name=self.__class__.__name__,
            start_time=self.start_time,
            end_time=end,
            duration=(end - self.start_time).total_seconds(),
            status=self.status,
            output_len=self.output_len
        )
        # metric.input.append(data['input'])
        metric.save()

    def process_pending(self):
        if self.input_type is dict:
            return
        pending_inputs = self.input_type.search().query(
            self.get_pending_query()
        )[:10000].execute().hits
        self.logger.info(f'Processing {len(pending_inputs)} pending inputs.')
        for pending in pending_inputs:
            self.process(pending)

    def start(self):  # pragma: no cover
        self.logger.debug('Filter started')
        if self.sync:
            while True:
                self.logger.debug("Fetching")
                try:
                    response = pubsub.subscriber.pull(
                        self.subscription_name(), max_messages=self.messages)
                except google.api_core.exceptions.NotFound:
                    self.logger.debug('Subscription not found')
                    time.sleep(10)
                    continue
                except google.api_core.exceptions.DeadlineExceeded:
                    self.logger.debug('Deadline')
                    continue

                self.logger.debug('Message received')
                for msg in response.received_messages:
                    self.callback(msg.message)
                ack_ids = [msg.ack_id for msg in response.received_messages]
                pubsub.subscriber.acknowledge(
                    self.subscription_name(), ack_ids)
        else:
            future = pubsub.subscriber.subscribe(
                self.subscription_name(), self.callback)
            future.result()

        self.logger.debug('Finish')


class ModelFunction(BaseFunction):
    model = None
    model_name = ''
    event_name = ''
    serializer = Serializer

    @classmethod
    def input_events(cls):
        return {
            cls.model_name + '.' + cls.event_name: cls.serializer
        }


class CreateFunction(ModelFunction):
    event_name = 'create'

    def call(self, input):
        self.serializer(data=input)
        input.save()
        yield (self.model_name + '.on_create', self.serializer(input).data)


class UpdateFunction(ModelFunction):
    event_name = 'update'

    def call(self, input):
        instance = self.model.objects.get(id=input.id)
        self.serializer(instance, data=input).save()
        yield (self.model_name + '.on_update', self.serializer(instance).data)


class DeleteFunction(ModelFunction):
    event_name = 'delete'

    def call(self, input):
        instance = self.model.objects.get(id=input.id)
        instance.delete()
        yield (self.model_name + '.on_delete', {'id': instance.id})
