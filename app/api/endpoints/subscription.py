# coding utf-8

from flask import request, current_app, g
from flask_restplus import Namespace, Resource, abort
from pynamodb.exceptions import DoesNotExist, DeleteError
from ..security import auth
from ..serializers.subscription import subscription_item_model, subscription_model, subscription_endpoint_model
from ...models import PushSubscription


ns = Namespace('subscription', description='Subscription related operations.')

@ns.route('')
class SubscriptionResource(Resource):
    decorators = [auth.login_required]

    @ns.expect(subscription_model)
    @ns.marshal_with(subscription_item_model)
    def post(self):
        """
        Add subscription
        """
        payload = request.json
        if PushSubscription.count(g.user['username'], PushSubscription.endpoint == payload['endpoint']) > 0:
            abort(409, 'Already exist')

        try:
            subscription = PushSubscription(
                owner=g.user['username'],
                endpoint=payload['endpoint'],
                expiration_time=int(payload['expiration_time']) if payload.get('expiration_time') else None,
                keys=payload['keys']
            )

            subscription.save()

            return subscription

        except Exception as ex:
            current_app.logger.error('Unable to add subscription for {0}'.format(ex))
            abort(400, 'Unable to add subscription, please try again later')

    @ns.expect(subscription_endpoint_model)
    @ns.response(404, 'Subscription not found')
    def delete(self):
        """
        Delete subscription
        """
        endpoint = request.json['endpoint']
        subscriptions = [p for p in PushSubscription.query(g.user['username'], PushSubscription.endpoint == endpoint)]
        if len(subscriptions) == 0:
            abort(404, 'Subscription not found')
        
        try:
            with PushSubscription.batch_write() as bach:
                for sub in subscriptions:
                    bach.delete(sub)
            
            return 'Subscription successfully deleted', 204
        
        except Exception as ex:
            current_app.logger.error('Unable to delete subscription {0}'.format(ex))
            abort(400, 'Unable to delete subscription, please try again later')
    