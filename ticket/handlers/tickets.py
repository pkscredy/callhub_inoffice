from ticket.dbapi import TicketActivityDbio
from ticket.models import TicketActivity


class TicketAct:
    def create_issue(self, data):
        tkt_data = {
            'subject': data.get('subject'),
            'content': data.get('content'),
            'department': data.get('department'),
            'category': data.get('category'),
            'urgent': data.get('urgent')
        }
        obj = TicketActivityDbio().create_obj(tkt_data)
        return {
            'message': 'Ticket has been raised successfully',
            'tkt_uuid': obj.uuid
        }

    def get_all_tickets(self):
        objs = TicketActivity.objects.all()
        if not objs:
            return {
                'message': 'No tickets are available'
            }
        tkt_list = []
        for obj in objs:
            tkt_data = {
                'tkt_uuid': obj.uuid
            }
            tkt_list.append(tkt_data)
        return tkt_list

    def get_with_state(self, dept=None, cat=None, state=None, urgent=None):
        if dept is not None:
            objs = TicketActivityDbio().filter_objects({'department': dept})
            return self.retrive_data(objs)
        elif cat is not None:
            objs = TicketActivityDbio().filter_objects({'category': cat})
            return self.retrive_data(objs)
        elif state is not None:
            objs = TicketActivityDbio().filter_objects({'status': state})
            return self.retrive_data(objs)
        else:
            objs = TicketActivityDbio().filter_objects({'urgent': urgent})
            return self.retrive_data(objs)

    def retrive_data(self, objs):
        issue_data = []
        for obj in objs:
            data = {
                'subject': obj.subject,
                'content': obj.content,
                'department': obj.department,
                'category': obj.category,
                'status': obj.status,
                'urgent': obj.urgent,
                'ticket_uuid': obj.uuid
            }
            issue_data.append(data)
        return issue_data

    def modify(self, ticket_uuid, data):
        obj = TicketActivityDbio().get_object(
            {
                'uuid': ticket_uuid
            }
        )
        tkt_data = {
            'subject': data.get('subject', obj.subject),
            'content': data.get('content', obj.content),
            'department': data.get('department', obj.department),
            'category': data.get('category', obj.category),
            'urgent': data.get('urgent', obj.urgent)
        }
        TicketActivityDbio().update_obj(obj, tkt_data)
        return {
            'message': 'Ticket has been modified',
            'ticket_uuid': obj.uuid
        }

    def delete_ticket(self, ticket_uuid):
        TicketActivityDbio().get_object(
            {
                'uuid': ticket_uuid
            }
        ).delete()
        return {
            'message': 'ticket deleted'
        }
