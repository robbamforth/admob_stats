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

## Configuration

You'll need:
- OAuth Client ID
- OAuth Client Secret  
- OAuth Refresh Token
- AdMob Publisher ID (pub-...)

See the [AdMob API docs](https://developers.google.com/admob/api/v1/auth) for setup.

## Sensors

Creates 16 sensors for earnings, impressions, ad requests, and clicks across today, yesterday, this month, and last month.
