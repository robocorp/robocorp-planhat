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
- [`types.Asset`](./planhat.types.md#class-asset): Assets in Planhat can represent many different things depending on your use case. It could be drones, if you're selling a drone tracking product, or it could be instances of your product in cases where a single customer can run multiple instances of your product in parallel. Assets could also represent your different products.
- [`types.Campaign`](./planhat.types.md#class-campaign): Manage campaigns you are running inside companies, e.g., to drive adoption or to deepen stakeholder relations.
- [`types.Churn`](./planhat.types.md#class-churn): Each time one of your customers churns or downgrades you can add a specific log about this. Mostly this "churn log" is added manually by the CSM from within Planhat, but there may also be times when you want to add it over API, for example if you're capturing information about downgrades and churn natively in-app in your own platform and want to send that over to Planhat.
- [`types.Company`](./planhat.types.md#class-company): Companies ("accounts"), are your customers. Depending on your business these might be agencies, schools, other businesses or something else. Companies can also be your previous customers and potentially future customers (prospects).
- [`types.Conversation`](./planhat.types.md#class-conversation): Conversations can be of different types such as email, chat, support tickets and manually logged notes. You can also create your own types in Planhat to represent things such as "in person meeting", "Training" etc. The default types (email, chat, ticket, call) are reserved and should not be created over API.
- [`types.CustomField`](./planhat.types.md#class-customfield): Most objects in Planaht can be customized by creating your own custom fields. Which model a given custom fields belongs is indicated by the parent property.
- [`types.DateTimeEncoder`](./planhat.types.md#class-datetimeencoder): A custom JSON encoder for use with Planhat objects.
- [`types.Enduser`](./planhat.types.md#class-enduser): An enduser represents an individual at one of your customers, typically a user of your product, a business contact or both. Endusers can automatically be created based on user tracking events, or based on conversations such as emails and tickets.
- [`types.Invoice`](./planhat.types.md#class-invoice): Invoices are normally generated automatically in Planhat when a license is created or renewed, invoices can include multiple line items. Planhat will not prepare invoices that you actually can send to your customers though. They're rather meant to help anyone working with your customers to know the status of current and past invoicing.
- [`types.Issue`](./planhat.types.md#class-issue): Issues typically represent Bugs or Feature Requests. Many of our customers fetch issues from Jira, but they can also be pushed to Planhat from other product management tools such as Product Board or Aha! You can also manage issues directly in Planhat without any external tool. Just keep in mind that the functionality is basic and mostly intended to contribute to the customer 360 view.
- [`types.License`](./planhat.types.md#class-license): Licenses represent your customers' subcriptions to your service and is the base for MRR (or ARR) calculations and most revenue reports. For non recurring revenue, please see the Sale (NRR) object. There are many ways to get license data into Planhat including incomming webhooks and CRM integrations. In some case though, you just want to handle it yourself over the api, for example if the main source of license data is your own system.
- [`types.NPS`](./planhat.types.md#class-nps): NPS records in Planhat represent the individual responses to an nps survey. Typically these are created automatically when running an nps campaign in Planhat, or in some cases imported from external NPS tools. A single enduser/contact can have multiple records if they responded to different surveys over time.
- [`types.NamedObjectMixin`](./planhat.types.md#class-namedobjectmixin): An abstract class representing objects that have a name.
- [`types.Note`](./planhat.types.md#class-note): Notes in Planhat are technically Conversations. You can create your own custom Touch Types to easily distinguish between different types of notes. You can also use custom fields to add more nuance to your Notes.
- [`types.Objective`](./planhat.types.md#class-objective): Being very clear and focused on your goals with customers is critical, and now you can track objectives and the health per objective.
- [`types.Opportunity`](./planhat.types.md#class-opportunity): Opportunities in Planhat represent a sales opportunity, whether it's selling to a new customer or more commonly a chance of expanding an existing account.
- [`types.PlanhatCompanyOwnedObject`](./planhat.types.md#class-planhatcompanyownedobject): An abstract class representing objects that are owned by a company.
- [`types.PlanhatIdType`](./planhat.types.md#class-planhatidtype)
- [`types.PlanhatObject`](./planhat.types.md#class-planhatobject): A base Planhat object. This is a dictionary with some additional
- [`types.PlanhatObjectList`](./planhat.types.md#class-planhatobjectlist): A list of Planhat objects.
- [`types.Project`](./planhat.types.md#class-project): Projects can represent many different real world objects with a natural start and stop date. A service provider for schools may use Projects to represent classes or courses. If you're selling a software to run sales competitions, then each competition may be a project.
- [`types.Sale`](./planhat.types.md#class-sale): The Sale (NRR) model represents not recurring revenue, like an onboarding fee, or a one-off professional services project.
- [`types.Task`](./planhat.types.md#class-task): Tasks are the things that you plan to do in the future. It can be a simple "to-do" without any specific due date, a reminder of something to be done at a specific point in time, or even a meeting with a start and end time.
- [`types.Ticket`](./planhat.types.md#class-ticket): Tickets in Planhat are Conversations, so if you plan to send tickets to Planhat via API then you can also use that endpoint. The ticket endpoint contains a bit of convenience logic for save tickets specificially, like setting the proper type automatically.
- [`types.User`](./planhat.types.md#class-user): Users are all your team members that need access to Planhat. Users can be created in the app, using spreadsheet upload or over api. If you're using teams to group your users in Planhat you'll need to call a separate endpoint to associate your Users with the right teams.
- [`types.Workspace`](./planhat.types.md#class-workspace): If you work with sub-instances at your customers, e.g., connecting with different departments or with different versions of your product (think like a Workspace in Slack), then this is the object to track that engagement!

## Functions

- No functions
