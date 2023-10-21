## Integration of Salesforce (external system) with local system

1) ### Potential Salesforce Integration:
<ul>
    <li>Salesforce Contact Object can be used to connect with our local Customer list as it offers similar functionality and has the required fields as well for intergation.</li>
    <li>Reference: <a href='https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_contact.htm'>https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_contact.htm</a></li>
</ul>

2) ### Environment Setup:
<ul>
    <li>The 'simple-salesforce' module can be used to interact with the Salesforce Contact Object through REST APIs.</li>
    <li>Reference: <a href='https://pypi.org/project/simple-salesforce/'>https://pypi.org/project/simple-salesforce/</a>
    <li>A developer account will be required along with credentials to login to the Salesforce instance through the module.</li>
</ul>

3) ### Integration Module:
<ul>
<li>Create a new module for the Salesforce integration (e.g., salesforce_integration.py).</li>
<li>Define functions and classes to interact with Salesforce, such as creating, reading, updating, and deleting customer records.</li>
</ul>

4) ### Customer Model:
<ul>
    <li>Create a corresponding Customer model in your application (e.g., SalesforceCustomer) that matches Salesforce's structure. It should inherit from a common Base model.</li>
</ul>

5) ### API Endpoints:
<ul>
    <li>Create API endpoints for Salesforce-related operations, similar to the ones we have for Stripe integration.</li>
    <li>These endpoints should handle the creation, retrieval, updating, and deletion of customer/contact records in Salesforce.</li>
</ul>

6) ### Kafka Topics:
<ul>
    <li>Establish separate Kafka topics for Salesforce events, such as salesforce-customer-created, salesforce-customer-updated, and salesforce-customer-deleted.</li>
    <li>This will help in the queueing of Salesforce events and their processing by the consumer/worker.</li>
</ul>

7) ### Producer:
<ul>
    <li>Create a separate producer for Salesforce events to ensure loose coupling.</li>
    <li>Implement logic to produce events when a customer is created, updated, or deleted in the local system, as well as when these actions happen in Salesforce.</li>
</ul>

8) ### Consumer:
<ul>
    <li>Create a new Kafka consumer to handle Salesforce events to ensure loose coupling.</li>
    <li>Implement event handlers to create, update, or delete customers in the local system based on Salesforce events.</li>
    <li>Ensure that the consumer can distinguish between events originating from Stripe and Salesforce.</li>
</ul>

9) ### Webhook Configuration:
<ul>
    <li>If Salesforce supports webhooks or push notifications, configure the application to listen for Salesforce events and translate them into Kafka messages.</li>
</ul>

10) ### Authentication and Authorization:
<ul>
    <li>Implement Salesforce authentication mechanisms to access Salesforce APIs securely.</li>
    <li>Ensure that user roles and permissions are well-defined for the Salesforce integration.</li>
</ul>

11) ### Testing:
<ul>
    <li>Extensively test the integration to ensure data consistency and error handling.</li>
    <li>Perform integration testing to confirm that both Stripe and Salesforce data is synchronized correctly.</li>
</ul>

12) ### Monitoring and Error Handling:
<ul>
    <li>Implement logging and monitoring to keep track of integration events and errors.</li>
    <li>Implement strategies to handle errors and exceptions.</li>
</ul>