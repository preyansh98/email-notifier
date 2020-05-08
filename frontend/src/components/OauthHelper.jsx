import React, {Component} from 'react';
import {Redirect} from 'react-router-dom';

/*
This component is used as an intermediary to get data from server on OAuth. 
Users are redirect to this URL after OAuth. 
OAuthHelper should fetch email token, validate, then pass as internal prop to Dashboard. 
*/
export default class OauthHelper extends Component { 
    state = {
        error : false,
        emailReceived : false, 
        email : ""
    }

    async componentDidMount(){
        const queryStr = window.location.search; 
        if(queryStr){
            const urlParams = new URLSearchParams(queryStr);
            if(urlParams.has('email')){
                const email = urlParams.get('email');
                this.setState({email : email}, () => {
                    this.setState({emailReceived : true})
                })
            } else {
                this.setState({error : true}); 
            }
        }
    }

    render(){
        return(
          <div>
              {this.state.error && (
                  <Redirect to="/"/>
              )}

              {this.state.emailReceived && (
                  <Redirect to = {{
                      pathname : '/dashboard',
                      state : { email : this.state.email }
                  }} />
              )}
          </div>  
        );
    }
}