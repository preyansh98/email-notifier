import React, {Component} from 'react'; 
import { Redirect } from 'react-router-dom';
import config from '../../config';

export default class DashboardMain extends Component { 
    state = {
        authenticated : null, 
        email : "",
        profile: null,
        job_status: null
    }

    async componentDidMount(){
        if(this.props.location && this.props.location.state.email){
            this.setState({authenticated : true}, () =>
                this.setState({email : this.props.location.state.email})); 

            this.fetchUser(); 
        } else {
            this.setState({authenticated : false})
        }
    }

    async fetchUser(){
        return await fetch(config.backendURLs.fetchUser, {
            headers : {
                'Accept' : 'application/json',
                'Content-type' : 'application-json',
                'email' : this.state.email
            },
            method : 'GET'
        })
        .then(res => {
            if(res.status === 200) {
                let resJson = res.json(); 

                this.setState({profile : resJson.profile});
                this.setState({job_status : resJson.job_status});   
            } 
        }).catch(function(err){
            console.error("Error fetching user profile!"); 
            //TODO: display error modal with go back prompt.
        })
    }
    
    render(){
        return(
            <div>
            {this.state.authenticated === false && (
                <div>Error you are not authenticated</div>
            )}

            {(this.state.authenticated) && (this.state.job_status!==null) && 
            (
                <div>
                    {this.state.job_status === "none" && (
                        <Redirect to={{
                            pathname: "/dashboard/new",
                            state : { authenticated : true}
                        }}/>
                    )}

                    {this.state.job_status === "active" && (
                        <Redirect to={{
                            pathname: "/dashboard/active",
                            state : { authenticated : true}
                        }}/>
                    )}     
                </div>
            )}

            </div>
        );
    }
}