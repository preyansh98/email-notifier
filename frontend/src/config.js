const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:5000"

export default {
    GOOGLE_OAUTH_HREF : BACKEND_URL + "/oauth-start",
};