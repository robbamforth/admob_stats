# AdMob Stats for Home Assistant

Monitor your Google AdMob statistics directly in Home Assistant with real-time earnings, impressions, ad requests, and click tracking.

## Features

- 16 real-time sensors tracking AdMob performance metrics
- Automatic data refresh for today, yesterday, this month, and last month
- OAuth 2.0 authentication for secure API access
- Easy installation via HACS or manual setup

## Installation

### HACS (Recommended)

1. Open HACS → Integrations
2. Click the three-dot menu (⋮) → Custom repositories
3. Add repository URL: `https://github.com/robbamforth/admob_stats`
4. Set category to **Integration**
5. Search for "AdMob Stats" and click **Download**
6. Restart Home Assistant
7. Add the integration via **Settings** → **Devices & Services** → **Add Integration**

### Manual Installation

1. Download and extract the latest release
2. Copy the `custom_components/admob_stats` folder to your Home Assistant `config` directory
3. Restart Home Assistant
4. Add the integration via **Settings** → **Devices & Services** → **Add Integration**

## Configuration

You'll need four credentials to configure this integration:

- **OAuth Client ID**
- **OAuth Client Secret**
- **OAuth Refresh Token**
- **AdMob Publisher ID** (format: `pub-XXXXXXXXXXXXXXXX`)

See the detailed setup guide below for instructions on obtaining these credentials.

## Available Sensors

The integration creates 16 sensors tracking the following metrics across multiple time periods:

**Metrics:**
- Earnings
- Impressions
- Ad requests
- Clicks

**Time Periods:**
- Today
- Yesterday
- This month
- Last month

---

## Setup Guide: Obtaining AdMob API Credentials

### 1. Get Your Publisher ID

1. Sign in to your [AdMob account](https://admob.google.com)
2. Navigate to **Settings** → **Account**
3. Copy your Publisher ID (format: `pub-XXXXXXXXXXXXXXXX`)

### 2. Create OAuth Client ID and Client Secret

#### Step 1: Create or Select a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. Sign in with the Google account linked to your AdMob account
3. Select an existing project or create a new one

#### Step 2: Enable AdMob API

1. In the Google Cloud Console, navigate to **APIs & Services** → **Library**
2. Search for "AdMob API"
3. Click **Enable**

#### Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** as the user type
3. Set publishing status to **Testing** (or **Published** if you prefer)
4. Fill in the required fields:
   - App name (e.g., "Home Assistant AdMob")
   - User support email
   - Developer contact email
5. If using Testing mode, add your Google account email as a test user
6. Click **Save and Continue** through the remaining screens

#### Step 4: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Select **Web application** as the application type
4. Enter a name (e.g., "Home Assistant AdMob OAuth")
5. Under **Authorized redirect URIs**, add: https://developers.google.com/oauthplayground
6. Click **Create**
7. Save the **Client ID** and **Client Secret** that appear

### 3. Generate Refresh Token

#### Step 1: Configure OAuth Playground

1. Go to the [Google OAuth Playground](https://developers.google.com/oauthplayground)
2. Click the gear icon (⚙️) in the top right
3. Check **"Use your own OAuth credentials"**
4. Enter your **Client ID** and **Client Secret** from the previous step
5. Set **Access type** to **Offline**
6. Set **OAuth flow** to **Server-side**

#### Step 2: Authorize AdMob API Access

1. In the left panel under **Step 1**, scroll down or search for: https://www.googleapis.com/auth/admob.readonly
You can also manually enter it in the "Input your own scopes" field
2. Click **Authorize APIs**
3. Sign in with your Google account (the one used for AdMob)
4. Click **Allow** to grant permissions

> **Note:** If you see `Error 403: access_denied`, see the Troubleshooting section below.

#### Step 3: Get the Refresh Token

1. Click **Exchange authorization code for tokens** (Step 2 on the left)
2. The **Refresh token** will appear in the response on the right side
3. Copy and save this refresh token securely

### 4. Configure the Home Assistant Integration

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "AdMob Stats"
4. Enter your credentials:
- **OAuth Client ID**: From Google Cloud Console
- **OAuth Client Secret**: From Google Cloud Console
- **OAuth Refresh Token**: From OAuth Playground
- **Publisher ID**: From AdMob account (format: `pub-XXXXXXXXXXXXXXXX`)

### Important Security Notes

- Keep your **Client Secret** and **Refresh Token** secure—they provide access to your AdMob data
- The refresh token is long-lived and won't expire as long as it's used periodically
- If your OAuth consent screen is in Testing mode, ensure your Google account is added as a test user
- The AdMob API has rate limits, but this integration polls at reasonable intervals to stay within them

---

## Troubleshooting

### Error 403: access_denied

This error occurs when your OAuth consent screen is in Testing mode, which restricts access to approved test users only.

#### Solution 1: Add Yourself as a Test User (Recommended)

1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** → **OAuth consent screen**
3. Scroll down to **Test users**
4. Click **Add Users**
5. Enter the exact email address of the Google account you're using for AdMob
6. Click **Save**
7. Return to the OAuth Playground and try authorizing again

#### Solution 2: Publish the OAuth App

If you don't want to manage test users, publish the app for personal use:

1. Go to **APIs & Services** → **OAuth consent screen**
2. Click **Publish App**
3. Confirm the action
4. You'll see an unverified app warning during authorization—this is normal for personal use
5. Click **Advanced** → **Go to [App Name] (unsafe)** to proceed

### Error: invalid_scope: Bad Request

This error typically occurs when API URLs are blocked on your network (e.g., by Pi-hole).

**Solution:** Whitelist the following domains in your network filtering software:

- `admob.googleapis.com`
- `oauth2.googleapis.com`
- `www.googleapis.com`
- `accounts.google.com`

---

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/robbamforth/admob_stats).

## License

This project is provided as-is for personal and commercial use with Home Assistant installations.


