# AdMob Stats for Home Assistant

Monitor your Google AdMob statistics in Home Assistant.

## Installation

### Via HACS (Recommended)

1. Open HACS → Integrations
2. Click ⋮ → Custom repositories
3. Add: `https://github.com/robbamforth/admob_stats`
4. Category: Integration
5. Find "Command Runner" and click Download
6. Restart Home Assistant

### Manual
1. Extract this ZIP file
2. Copy the `custom_components/admob_stats` folder to your Home Assistant config
3. Restart Home Assistant
4. Add the integration via UI (Settings > Integrations)
<BR><BR><BR>
## Configuration

You'll need:
- OAuth Client ID
- OAuth Client Secret  
- OAuth Refresh Token
- AdMob Publisher ID (pub-...)

See the [AdMob API docs](https://developers.google.com/admob/api/v1/auth) for setup.

<BR><BR><BR>
## Sensors

Creates 16 sensors for earnings, impressions, ad requests, and clicks across today, yesterday, this month, and last month.


<BR><BR><BR>
## How To Get Login Details

### Setting Up AdMob API Credentials for Home Assistant

To configure the AdMob Stats integration, you need four credentials from Google Cloud and AdMob. Here's how to obtain each one:

### 1. Get Your Publisher ID
This is the easiest credential to find.
1.	Sign in to your AdMob account at https://admob.google.com
2.	Click Settings in the sidebar
3.	Click Account
4.	Your Publisher ID will be displayed (format: pub-XXXXXXXXXXXXXXXX)


### 2. Create OAuth Client ID and Client Secret
You need to create OAuth 2.0 credentials in Google Cloud Console.

#### Step 1: Create/Select a Google Cloud Project
1.	Go to the Google Cloud Console: https://console.cloud.google.com
2.	Sign in with the same Google account linked to your AdMob account
3.	Either select an existing project or create a new one

#### Step 2: Enable AdMob API
1.	In the Google Cloud Console, search for "AdMob API" in the API Library
2.	Click Enable if it's not already enabled

#### Step 3: Configure OAuth Consent Screen
1.	Go to APIs & Services > OAuth consent screen
2.	Set User type to External
3.	Set Publishing status to Testing (or Published if you prefer)
4.	Fill in required fields:
  o	App name (e.g., "Home Assistant AdMob")
  o	User support email
  o	Developer contact email
5.	If using Testing mode, add your Google account email as a test user
6.	Click Save and Continue through the remaining screens

#### Step 4: Create OAuth Credentials
1.	Go to APIs & Services > Credentials
2.	Click Create Credentials > OAuth client ID
3.	Select Web application as the application type
4.	Give it a name (e.g., "Home Assistant AdMob OAuth")
5.	Under Authorized redirect URIs, add:
  https://developers.google.com/oauthplayground
6.	Click Create
7.	Save the Client ID and Client Secret that appear - you'll need these


### 3. Generate Refresh Token
The refresh token allows the integration to access your AdMob data long-term without repeated logins.

#### Step 1: Configure OAuth Playground
1.	Go to Google OAuth Playground
2.	Click the gear icon (⚙️) in the top right
3.	Check "Use your own OAuth credentials"
4.	Enter your Client ID and Client Secret from step 2
5.	Set Access type to Offline
6.	Set OAuth flow to Server-side

#### Step 2: Authorize AdMob API Access
1.	In the left panel under Step 1, scroll down or use the search box to find:
  https://www.googleapis.com/auth/admob.readonly
  Or manually enter it in the "Input your own scopes" field
3.	Click Authorize APIs
4.	Sign in with your Google account (same one used for AdMob)
5.	Click Allow to grant permissions

NOTE: if you see 'Error 403: access_denied', see troubleshppting below.

#### Step 3: Get the Refresh Token
1.	Click Exchange authorization code for tokens (Step 2 on the left)
2.	The Refresh token will appear in the response on the right side
3.	Copy and save this refresh token - this is what you'll use in Home Assistant
4. Configure Home Assistant Integration

Now you have all four credentials needed:
1.	In Home Assistant, go to Settings > Devices & Services
2.	Click Add Integration
3.	Search for "AdMob Stats"
4.	Enter the credentials:
  o	OAuth Client ID: From Google Cloud Console
  o	OAuth Client Secret: From Google Cloud Console
  o	OAuth Refresh Token: From OAuth Playground
  o	Publisher ID: From AdMob account (pub-XXXXXXXXXXXXXXXX)


#### Important Notes
•	Keep your Client Secret and Refresh Token secure - they provide access to your AdMob data<BR>
•	The refresh token is long-lived and won't expire as long as you use it periodically<BR>
•	If you set your OAuth consent screen to "Testing" mode, make sure your Google account is added as a test user<BR>
•	The AdMob API has rate limits, but the integration polls at reasonable intervals to stay within limits<BR>

<BR><BR><BR>
### Troubleshooting

#### Error 403: access_denied

This error occurs because your OAuth consent screen is in "Testing" mode, which restricts access to only approved test users. Here's how to fix it:

#### Solution 1: Add Yourself as a Test User (Quickest)
1.	Go to Google Cloud Console
2.	Navigate to APIs & Services > OAuth consent screen
3.	Scroll down to Test users
4.	Click Add Users
5.	Enter the exact email address of the Google account you're using for AdMob and OAuth Playground
6.	Click Save
7.	Go back to the OAuth Playground and try authorizing again

#### Solution 2: Publish the OAuth App (Alternative)
If you don't want to manage test users, you can publish the app for personal use:
1.	Go to APIs & Services > OAuth consent screen
2.	Click Publish App
3.	Confirm the action
4.	You'll see a warning that it's unverified - this is fine for personal use
5.	Users (including you) will see a warning screen during authorization, but you can click Advanced > Go to [App Name] (unsafe) to proceed



