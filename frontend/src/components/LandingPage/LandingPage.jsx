import React, { Component } from "react";
import { Card, Button } from "react-bootstrap";
import { FaGoogle, FaHeart, FaGithub } from "react-icons/fa";
import { MdUnfoldMore, MdHelp, MdFeedback } from "react-icons/md";
import { Fab, Action } from "react-tiny-fab";
import "react-tiny-fab/dist/styles.css";
import config from '../../config';

export default class LandingPage extends Component {
  state = {};

  render() {
    return (
      <div>
        <center>
          <Card bg="dark" text="white" style={styles.cardStyle}>
            <Card.Body>
              <Card.Title>Welcome to Email Notifier!</Card.Title>
              <br />

              <Card.Text>
                Tired of constantly refreshing your inbox waiting for an important email? 
              </Card.Text>
            <Card.Text>
                Email Notifier lets you receive real-time updates about specific emails by sending you an automated Phone Call and SMS Message. 
                Use Email Notifier and never worry about missing important updates anymore.
                </Card.Text>
              <br />
              <br />
              <br />
              <Button variant="light" size="lg" href={config.GOOGLE_OAUTH_HREF}>
                <FaGoogle size="18px" /> | Sign In With Google
              </Button>
            </Card.Body>
            <Card.Footer>
              <small className="text-muted">
                <a href = "https://github.com/preyansh98/email-notifier" target="_blank" rel = "noopener noreferrer" style={{color:"white"}}><FaGithub/>  </a> 
                <font color = "white">| Made with <FaHeart/> by Preyansh Kaushik </font> 
              </small>
            </Card.Footer>
          </Card>

          <Fab
            mainButtonStyles={styles.fab.mainButtonStyles}
            actionButtonStyles={styles.fab.actionButtonStyles}
            position={styles.fab.position}
            icon={<MdUnfoldMore />}
            event="hover"
          >
            <Action
              style={styles.fab.actionButtonStyles}
              text="Help"
              onClick={(e) => {
                e.preventDefault();
              }}
            >
              <MdHelp />
            </Action>
            <Action
              style={styles.fab.actionButtonStyles}
              text="Give Feedback"
              onClick={(e) => {
                e.preventDefault();
              }}
            >
              <MdFeedback />
            </Action>
          </Fab>
        </center>
      </div>
    );
  }
}

const styles = {
  cardStyle: {
    width: "40%",
    height: "500px",
    display: "flex",
    marginTop: "10%",
  },
  fab: {
    position: {
      bottom: 10,
      right: 10,
    },
    mainButtonStyles: {
      backgroundColor: "#27ae60",
    },
    actionButtonStyles: {
      backgroundColor: "#16a085",
    },
  }
};
