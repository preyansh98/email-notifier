import React, {Component} from 'react'; 

export default class DashboardMain extends Component { 
    state = {
        authenticated : "notready", 
        email : ""
    }

    async componentDidMount(){
        if(this.props.location && this.props.location.state.email){
            this.setState({authenticated : true}, () =>
                this.setState({email : this.props.location.state.email})); 
        } else {
            this.setState({authenticated : false})
        }
    }
    
    render(){
        return(
            <div>
            {this.state.authenticated == false && (
                <div>Error you are not authenticated</div>
            )}

            {this.state.authenticated && (
                <div>
                    {/* Fetch profile, if has jobs active redir to active */}
                    {/* If no jobs active, then move to newuser flow */ }
                </div>
            )}

            </div>
        );
    }
}