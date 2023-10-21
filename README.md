# Zenskar-Two-Way-Sync-App

### System environment:
1) Windows 11
2) Anaconda Python 3.10.9
3) Docker Desktop
4) MySQL 8.0
5) ngrok

### Installation steps:
1) Clone the repository:
   
   ```bash
   git clone https://github.com/atharvabhide/Zenskar-Two-Way-Sync-App.git
   ```
   
2) Install dependencies:
    
   ```bash
   cd Zenskar-Two-Way-Sync-App
   pip install -r requirements.txt
   ```
   
3) Create a developer account on Stripe and copy the Secret key: <a href='https://dashboard.stripe.com/developers'>https://dashboard.stripe.com/developers</a>

4) Create the MySQL DB:
   ```bash
   mysql -u <DB_USERNAME> -p
   create database <DB_NAME>
   ```

5) Create an env file in the root folder:
   
   ```bash
   DB_USERNAME = <YOUR_DB_USERNAME>
   DB_PASSWORD = <YOUR_DB_PASSWORD>
   DB_NAME = <YOUR_DB_NAME>
   STRIPE_API_KEY = <YOUR_STRIPE_API_PRIVATE_KEY>
   ```

6) Create and start Docker containers for Kafka and Zookeeper:
   ```bash
   docker-compose -f backend/kafka/docker_compose.yml up -d
   ```

7) Expose port 8000 using ngrok:
   ```bash
   ngrok http 8000
   ```
   
8) Add the ngrok exposed url in the Web Hooks section of the Stripe Developer account: <a href='https://dashboard.stripe.com/test/webhooks'>https://dashboard.stripe.com/test/webhooks</a> with the following events:
   <ul>
   <li>customer.created</li>
   <li>customer.updated</li>
   <li>customer.deleted</li>
   </ul> 
  
9) Run the main FastAPI local server (in a separate terminal):
   ```bash
   python backend\main.py
   ```

10) Run the stripe webhook FastAPI local server (in a separate terminal):
      ```bash
      python backend\kafka\api.py
      ```

11) Run the main Kafka consumer/worker (in a separate terminal):
      ```bash
      python backend\kafka\consumer.py
      ```
 
12) Run the stripe webhook consumer/worker (in a separate terminal):
      ```bash
      python backend\kafka\stripe_consumer.py
      ```

13) Outward Sync:
    <ul>
      <li>Open localhost:8080/docs to access the FastAPI documentation.</li>
      <li>Perform CRUD operations by using the APIs.</li>
      <li>The changes get reflected in the Customer list of the developer account on Stripe.</li>
    </ul>

14) Inward Sync:
    <ul>
      <li>Open Customer list of the developer account on Stripe.</li>
      <li>Perform CRUD operations through the Stripe interface.</li>
      <li>The changes get reflected on the local system and can be observed on localhost:8080/docs through the read APIs.</li>
    </ul>
