# SGMT Lambda Deployment Guide

**Project Name:** SteamGifts Group Management Tool (SGMT) – AWS Lambda Edition

## Deployment Steps

### 1. Configure Database Access
Update the `application.config` file with your MySQL database credentials and schema name under the `[MySql]` section.  
The Lambda function uses these settings to connect to the database. Ensure the database contains the SGMT schema and data (you can import it from the original tool).

---

### 2. Install Python Dependencies
This project requires the following packages:
- `pymysql`
- `requests`
- `beautifulsoup4`

Create a file called `requirements.txt` with:

```txt
pymysql
requests
beautifulsoup4
```

Then install these packages into a local directory called `package`:

```bash
pip install -r requirements.txt -t package/
```

Copy your source code into that folder:

```bash
cp *.py package/
cp application.config package/
```

Then create the deployment ZIP:

```bash
cd package
zip -r ../SGMTLambda.zip .
```

---

### 3. Upload to AWS Lambda
- Create a new AWS Lambda function (Python 3.x runtime).
- Set the handler to: `lambda_function.lambda_handler`
- Upload `SGMTLambda.zip` through the console or run:

```bash
aws lambda update-function-code --function-name your_lambda_name --zip-file fileb://SGMTLambda.zip
```

---

### 4. Set Environment Variables (Optional)
If you prefer not to include `application.config`, you can set DB credentials via Lambda environment variables and modify `MySqlConnector.py` to read from `os.environ`.

---

### 5. Configure Networking (If Needed)
If your MySQL database is inside a **VPC** (e.g., RDS without public access), configure the Lambda function to run in that VPC and attach the correct subnets and security groups.  
Ensure the security group allows **inbound MySQL (port 3306)** from Lambda's private IP.

---

### 6. API Gateway Setup
Create an **HTTP API** or **REST API** (recommended: HTTP API) to route requests to this Lambda.

Recommended setup:
- Create a route: `/SGMT/{proxy+}`
- Integration target: Lambda function
- Enable **Lambda Proxy integration**
- Deploy the API to a stage (e.g., `prod`)
- You will now be able to access endpoints like:

```
https://your-api-id.amazonaws.com/prod/SGMT/UserCheckFirstGiveaway
```

Supported routes include:
- `/SGMT-Admin/GroupUsersCheckRules`
- `/SGMT-Admin/Test`
- `/SGMT/legal`
- `/SGMT/servicecheck`
- `/SGMT/CheckMonthly`
- `/SGMT/CheckAllGiveawaysAccordingToRules`
- `/SGMT/UserCheckFirstGiveaway`
- `/SGMT/UserFullGiveawaysHistory`
- `/SGMT/GroupUsersSummary`
- `/SGMT/UserCheckRules`
- `/SGMT/PopularGiveaways`
- `/SGMT/CheckGameGiveaways`
- `/SGMT/GetAvailableGroups`

---

### 7. Test the Endpoints
After deployment:
- `/SGMT/servicecheck` should return `"OK"`
- `/SGMT/GetAvailableGroups` should return HTML group info
- Other endpoints return formatted HTML — view them in a browser

---

## Notes

- **HTML Responses:** Lambda responses set `Content-Type: text/html`. API Gateway passes them through, so they can be viewed in a browser.
- **Logging:** Lambda logs go to CloudWatch automatically. Use `LogUtils` output to debug or monitor.
- **Security:** Never commit sensitive credentials. If using `application.config`, ensure it is read-only. Alternatively, use AWS Secrets Manager or encrypted environment variables.
- **Data Freshness:** You may need to run update jobs (e.g., `UpdateGroupData`) manually or on a schedule to refresh database content.

---

## Final Thoughts

With proper packaging and API Gateway routing, all SGMT tools become accessible as web endpoints. Keep your database clean and logs monitored to ensure long-term reliability.
