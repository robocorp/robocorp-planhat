<!-- markdownlint-disable -->

# API Overview

## Modules

- [`planhat`](./planhat.md#module-planhat): Planhat API library for the Robocorp Python Automation Framework
- [`planhat.client`](./planhat.client.md#module-planhatclient)
- [`planhat.errors`](./planhat.errors.md#module-planhaterrors)
- [`planhat.session`](./planhat.session.md#module-planhatsession): Provides Planhat session functionality.
- [`planhat.types`](./planhat.types.md#module-planhattypes): Data types used in the Planhat client.

## Classes

- [`client.PlanhatClient`](./planhat.client.md#class-planhatclient): Automation class to interact with the Planhat API.
- [`errors.PlanhatAuthConfigurationError`](./planhat.errors.md#class-planhatauthconfigurationerror): Error when authentication is not configured correctly.
- [`errors.PlanhatAuthFailedError`](./planhat.errors.md#class-planhatauthfailederror): Error when authentication fails or the API server returns a 403 error.
- [`errors.PlanhatBadRequestError`](./planhat.errors.md#class-planhatbadrequesterror): Error when the API server returns a 400 error.
- [`errors.PlanhatHTTPError`](./planhat.errors.md#class-planhathttperror): Base class for all Planhat API Session errors.
- [`errors.PlanhatNotFoundError`](./planhat.errors.md#class-planhatnotfounderror): Error when the requested resource is not found.
- [`errors.PlanhatRateLimitError`](./planhat.errors.md#class-planhatratelimiterror): Error when the API's rate limits are exceeded.
- [`errors.PlanhatServerError`](./planhat.errors.md#class-planhatservererror): Error when the API server returns a 5xx error.
- [`client.PlanhatClient`](./planhat.client.md#class-planhatclient): Automation class to interact with the Planhat API.
- [`errors.PlanhatAuthConfigurationError`](./planhat.errors.md#class-planhatauthconfigurationerror): Error when authentication is not configured correctly.
- [`errors.PlanhatAuthFailedError`](./planhat.errors.md#class-planhatauthfailederror): Error when authentication fails or the API server returns a 403 error.
- [`errors.PlanhatBadRequestError`](./planhat.errors.md#class-planhatbadrequesterror): Error when the API server returns a 400 error.
- [`errors.PlanhatError`](./planhat.errors.md#class-planhaterror): Base class for all Planhat API errors.
- [`errors.PlanhatHTTPError`](./planhat.errors.md#class-planhathttperror): Base class for all Planhat API Session errors.
- [`errors.PlanhatNotFoundError`](./planhat.errors.md#class-planhatnotfounderror): Error when the requested resource is not found.
- [`errors.PlanhatRateLimitError`](./planhat.errors.md#class-planhatratelimiterror): Error when the API's rate limits are exceeded.
- [`errors.PlanhatServerError`](./planhat.errors.md#class-planhatservererror): Error when the API server returns a 5xx error.
- [`session.PlanhatAuth`](./planhat.session.md#class-planhatauth): Attaches HTTP Authorization to the given Request object.
- [`session.PlanhatSession`](./planhat.session.md#class-planhatsession): A Planhat session.
- [`types.Asset`](./planhat.types.md#class-asset): Assets in Planhat can represent many different things depending on your use case.
- [`types.Campaign`](./planhat.types.md#class-campaign): Manage campaigns you are running inside companies, e.g., to drive adoption
- [`types.Churn`](./planhat.types.md#class-churn): Each time one of your customers churns or downgrades you can add a specific
- [`types.Company`](./planhat.types.md#class-company): Class to represent Companies ("accounts"), which are your customers.
- [`types.Conversation`](./planhat.types.md#class-conversation): Represents conversations of different types.
- [`types.CustomField`](./planhat.types.md#class-customfield): Represents custom fields in Planhat.
- [`types.DateTimeEncoder`](./planhat.types.md#class-datetimeencoder): A custom JSON encoder for use with Planhat objects.
- [`types.Enduser`](./planhat.types.md#class-enduser): Represents an individual at one of your customers. This could be a user of
- [`types.Invoice`](./planhat.types.md#class-invoice): Represents Invoices in Planhat.
- [`types.Issue`](./planhat.types.md#class-issue): Issues typically represent Bugs or Feature Requests. Many of our customers
- [`types.License`](./planhat.types.md#class-license): Represents your customers' subscriptions to your service. This is the base
- [`types.NPS`](./planhat.types.md#class-nps): Represents the individual responses to an NPS survey in Planhat. These are
- [`types.NamedObjectMixin`](./planhat.types.md#class-namedobjectmixin)
- [`types.Note`](./planhat.types.md#class-note): Notes in Planhat are technically Conversations. You can create your own
- [`types.Objective`](./planhat.types.md#class-objective): Represents the objectives and their health in Planhat.
- [`types.Opportunity`](./planhat.types.md#class-opportunity): Represents a sales opportunity in Planhat. This could be a chance to sell to
- [`types.PlanhatCompanyOwnedObject`](./planhat.types.md#class-planhatcompanyownedobject): An abstract class representing objects that are owned by a company.
- [`types.PlanhatIdType`](./planhat.types.md#class-planhatidtype)
- [`types.PlanhatObject`](./planhat.types.md#class-planhatobject): A base Planhat object. This is a dictionary with some additional
- [`types.PlanhatObjectList`](./planhat.types.md#class-planhatobjectlist): A list of Planhat objects.
- [`types.Project`](./planhat.types.md#class-project): Represents Projects in Planhat.
- [`types.Sale`](./planhat.types.md#class-sale): The Sale (NRR) model represents not recurring revenue, like an onboarding
- [`types.Task`](./planhat.types.md#class-task): Represents tasks in Planhat. Tasks are future actions, which can be simple
- [`types.Ticket`](./planhat.types.md#class-ticket): Tickets in Planhat are Conversations. If you plan to send tickets to Planhat
- [`types.User`](./planhat.types.md#class-user): Represents a User in Planhat.
- [`types.Workspace`](./planhat.types.md#class-workspace): If you work with sub-instances at your customers, e.g., connecting

## Functions

- No functions
