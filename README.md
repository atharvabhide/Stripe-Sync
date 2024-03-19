# StripeSync

### Demo Video:

https://github.com/atharvabhide/StripeSync/assets/67187699/61e36a65-82bb-4149-9823-69a448db068b


### System environment:
1) Windows 11
2) Anaconda Python 3.10.9 / Python 3.10.9 virtual environment (<a href='https://www.anaconda.com/download'>Link</a>)
3) Docker Desktop (<a href='https://www.docker.com/products/docker-desktop/'>Link</a>)
4) MySQL 8.0 (<a href='https://dev.mysql.com/downloads/mysql/'>Link</a>)
5) ngrok (<a href='https://ngrok.com/download'>Link</a>)

### Installation steps:
1) Clone the repository:
   
   ```bash
   git clone https://github.com/atharvabhide/Zenskar-Two-Way-Sync-App.git
   cd Zenskar-Two-Way-Sync-App
   ```

2) Create a Python environment

   ```bash
   conda create --name <ENV_NAME> python=3.10.9
   conda activate <ENV_NAME>

   OR

   virtualenv <ENV_NAME> -p python3.10.9
   <ENV_NAME>\Scripts\activate
   
3) Install dependencies:
    
   ```bash
   pip install -r requirements.txt
   ```
   
4) Create a developer account on Stripe and copy the Secret key: <a href='https://dashboard.stripe.com/developers'>https://dashboard.stripe.com/developers</a>

5) Create the MySQL DB:
   ```bash
   mysql -u <DB_USERNAME> -p
   create database <DB_NAME>
   ```

6) Create an env file in the backend folder (.env):
   
   ```bash
   DB_USERNAME = <YOUR_DB_USERNAME>
   DB_PASSWORD = <YOUR_DB_PASSWORD>
   DB_NAME = <YOUR_DB_NAME>
   STRIPE_API_KEY = <YOUR_STRIPE_API_PRIVATE_KEY>
   ```

7) Create and start Docker containers for Kafka and Zookeeper:
   ```bash
   docker-compose -f backend\kafka\docker_compose.yml up -d
   ```

8) Expose port 8000 using ngrok:
   ```bash
   ngrok http 8000
   ```
   
9) Add the ngrok exposed url (add /stripe-webhook to the url) in the Web Hooks section of the Stripe Developer account: <a href='https://dashboard.stripe.com/test/webhooks'>https://dashboard.stripe.com/test/webhooks</a> with the following events:
   <ul>
   <li>customer.created</li>
   <li>customer.updated</li>
   <li>customer.deleted</li>
   </ul> 
  
10) Run the main FastAPI local server (in a separate terminal):
      ```bash
      python backend\main.py
      ```

11) Run the stripe webhook FastAPI local server (in a separate terminal):
      ```bash
      python backend\kafka\api.py
      ```

12) Run the main Kafka consumer/worker (in a separate terminal):
      ```bash
      python backend\kafka\consumer.py
      ```
 
13) Run the stripe webhook Kafka consumer/worker (in a separate terminal):
      ```bash
      python backend\kafka\stripe_consumer.py
      ```

14) Outward Sync:
    <ul>
      <li>Open localhost:8080/docs to access the FastAPI documentation.</li>
      <li>Perform CRUD operations by using the APIs.</li>
      <li>The changes get reflected in the Customer list of the developer account on Stripe.</li>
    </ul>

15) Inward Sync:
    <ul>
      <li>Open Customer list of the developer account on Stripe.</li>
      <li>Perform CRUD operations through the Stripe interface.</li>
      <li>The changes get reflected on the local system and can be observed on localhost:8080/docs through the read APIs.</li>
    </ul>

16) To use the Streamlit dashboard for the outward sync (in a separate terminal):
      ```bash
      streamlit run frontend\app.py
      ```
