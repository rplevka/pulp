from gettext import gettext as _

from pulp.client.commands.schedule import (
    DeleteScheduleCommand, ListScheduleCommand, CreateScheduleCommand,
    UpdateScheduleCommand, NextRunCommand, ScheduleStrategy)

from pulp_node import constants
from pulp_node.error import CLI_DEPRECATION_WARNING
from pulp_node.extensions.admin.options import (NODE_ID_OPTION, MAX_BANDWIDTH_OPTION,
                                                MAX_CONCURRENCY_OPTION)


DESC_LIST = _('list scheduled sync operations')
DESC_CREATE = _('adds a new scheduled sync operation')
DESC_DELETE = _('delete a sync schedule')
DESC_UPDATE = _('updates an existing schedule')
DESC_NEXT_RUN = _('displays the next scheduled sync run for a child node')

# A node sync is considered an update operation on the REST API
SYNC_OPERATION = 'update'


class NodeListScheduleCommand(ListScheduleCommand):
    def __init__(self, context):
        strategy = NodeSyncScheduleStrategy(context)
        super(self.__class__, self).__init__(context, strategy, description=DESC_LIST)
        self.add_option(NODE_ID_OPTION)

    def run(self, **kwargs):
        self.context.prompt.render_warning_message(CLI_DEPRECATION_WARNING)
        super(NodeListScheduleCommand, self).run(**kwargs)


class NodeCreateScheduleCommand(CreateScheduleCommand):
    def __init__(self, context):
        strategy = NodeSyncScheduleStrategy(context)
        super(self.__class__, self).__init__(context, strategy, description=DESC_CREATE)
        self.add_option(NODE_ID_OPTION)
        self.add_option(MAX_BANDWIDTH_OPTION)
        self.add_option(MAX_CONCURRENCY_OPTION)

    def run(self, **kwargs):
        self.context.prompt.render_warning_message(CLI_DEPRECATION_WARNING)
        super(NodeCreateScheduleCommand, self).run(**kwargs)


class NodeDeleteScheduleCommand(DeleteScheduleCommand):
    def __init__(self, context):
        strategy = NodeSyncScheduleStrategy(context)
        super(self.__class__, self).__init__(context, strategy, description=DESC_DELETE)
        self.add_option(NODE_ID_OPTION)

    def run(self, **kwargs):
        self.context.prompt.render_warning_message(CLI_DEPRECATION_WARNING)
        super(NodeDeleteScheduleCommand, self).run(**kwargs)


class NodeUpdateScheduleCommand(UpdateScheduleCommand):
    def __init__(self, context):
        strategy = NodeSyncScheduleStrategy(context)
        super(self.__class__, self).__init__(context, strategy, description=DESC_UPDATE)
        self.add_option(NODE_ID_OPTION)

    def run(self, **kwargs):
        self.context.prompt.render_warning_message(CLI_DEPRECATION_WARNING)
        super(NodeUpdateScheduleCommand, self).run(**kwargs)


class NodeNextRunCommand(NextRunCommand):
    def __init__(self, context):
        strategy = NodeSyncScheduleStrategy(context)
        super(self.__class__, self).__init__(context, strategy, description=DESC_NEXT_RUN)
        self.add_option(NODE_ID_OPTION)

    def run(self, **kwargs):
        self.context.prompt.render_warning_message(CLI_DEPRECATION_WARNING)
        super(NodeNextRunCommand, self).run(**kwargs)


class NodeSyncScheduleStrategy(ScheduleStrategy):

    # See super class for method documentation

    def __init__(self, context):
        super(self.__class__, self).__init__()
        self.context = context
        self.api = context.server.consumer_content_schedules

    def create_schedule(self, schedule, failure_threshold, enabled, kwargs):
        node_id = kwargs[NODE_ID_OPTION.keyword]
        max_bandwidth = kwargs[MAX_BANDWIDTH_OPTION.keyword]
        max_concurrency = kwargs[MAX_CONCURRENCY_OPTION.keyword]
        units = [dict(type_id='node', unit_key=None)]
        options = {
            constants.MAX_DOWNLOAD_BANDWIDTH_KEYWORD: max_bandwidth,
            constants.MAX_DOWNLOAD_CONCURRENCY_KEYWORD: max_concurrency,
        }
        return self.api.add_schedule(
            SYNC_OPERATION,
            node_id,
            schedule,
            units,
            failure_threshold,
            enabled,
            options)

    def delete_schedule(self, schedule_id, kwargs):
        node_id = kwargs[NODE_ID_OPTION.keyword]
        return self.api.delete_schedule(SYNC_OPERATION, node_id, schedule_id)

    def retrieve_schedules(self, kwargs):
        node_id = kwargs[NODE_ID_OPTION.keyword]
        return self.api.list_schedules(SYNC_OPERATION, node_id)

    def update_schedule(self, schedule_id, **kwargs):
        node_id = kwargs.pop(NODE_ID_OPTION.keyword)
        return self.api.update_schedule(SYNC_OPERATION, node_id, schedule_id, **kwargs)

    def run(self, **kwargs):
        self.context.prompt.render_warning_message(CLI_DEPRECATION_WARNING)
        super(NodeSyncScheduleStrategy, self).run(**kwargs)
