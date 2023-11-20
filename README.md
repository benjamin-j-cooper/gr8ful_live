# gr8ful_live
Gr8ful Live is a live music app that tracks shows of your favorite artists from Spotify and sends a monthly email with upcoming concerts in your area for artists you love. 

## Usage
### Create Spotify API App:
In order to use this app, you will first need to set up a Spotify account. Once you have a spotify account, login to [Spotify for Developers](https://developer.spotify.com) with your Spotify credentials.
* Navigate to your developer dashboard
* Create New App
* Give your app a name, description, select the type (Web API), and specify a generic redirect URL `http://localhost:8080`
* Once you have created your app, click on the app and navigate to settings.
* Copy the Client_ID and Client_Secret
* Save these as credentials.json in your project directory:  
    `{`  
    &nbsp;&nbsp;&nbsp;&nbsp;`"spotify_api": {`  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"CLIENT_ID" : "your_client_id_here",`  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"CLIENT_SECRET" : "your_client_secret_here",`  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"REDIRECT" : "http://localhost:8080"`  
    &nbsp;&nbsp;&nbsp;&nbsp;`}`  
    `}`  
