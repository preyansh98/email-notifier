const BACKEND_BASE_URL = process.env.BACKEND_BASE_URL || "http://localhost:5000"

export default {
    GOOGLE_OAUTH_HREF : BACKEND_BASE_URL + "/oauth-start",

    backendURLs : {
        fetchUser : BACKEND_BASE_URL + "/user/fetch" 
    }
};