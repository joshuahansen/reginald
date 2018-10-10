import React, { Component } from 'react';
import './App.css';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';


const theme = createMuiTheme ({
    palette: {
        primary: { main: '#e60228'},
        secondary: { main: '#448aff'},
    },
});

const rows = []

class App extends Component {

  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.retrieve = this.retrieve.bind(this);
    this.handleEncode =this.handleEncode.bind(this);
    this.handleInput = this.handleInput.bind(this);
    this.state = {
      rows: null,
      open: false,
    };
  }

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  handleSubmit() {

    console.log("test3")
    var name = document.getElementById('formName').value;
    var url = "http://123.243.247.182:5000/register?name=";
    var fullURL = url.concat(name);
    var request = new XMLHttpRequest();
    request.open('GET', fullURL, true);

    request.onload = function () {

      console.log("test2")
      var data = JSON.parse(this.response);

      if (request.status === 200) {

        data.forEach(d => {

          console.log("test1")
          console.log(d);

        });

      } else {
        console.log('error');
      }

    }
    request.send();

  };

  handleEncode() {

    console.log("Encode");

    var url = "http://123.243.247.182:5000/train";
    var request = new XMLHttpRequest();
    request.open('GET', url, true);

    request.onload = function () {

      var data = JSON.parse(this.response);

      if (request.status === 200) {

        data.forEach(d => {

          console.log(d);

        });

      } else {
        console.log('error');
      }

    }
    request.send();
    this.setState({ open: false });
  };

  handleStartRec() {

    console.log("Start");

    var url = "http://123.243.247.182:5000/recognize";
    var request = new XMLHttpRequest();
    request.open('GET', url, true);

    request.onload = function () {

      var data = JSON.parse(this.response);

      if (request.status === 200) {

        data.forEach(d => {

          console.log(d);

        });

      } else {
        console.log('error');
      }

    }
    request.send();

  };

  handleStopRec() {

    console.log("Stop");

    var url = "http://123.243.247.182:5000/stop-recognize";
    var request = new XMLHttpRequest();
    request.open('GET', url, true);

    request.onload = function () {

      var data = JSON.parse(this.response);

      if (request.status === 200) {

        data.forEach(d => {

          console.log(d);

        });

      } else {
        console.log('error');
      }

    }
    request.send();

  };

  handleInput() {


    console.log("Input Test");
    var AWS = require('aws-sdk');

    AWS.config.update({
      accessKeyId: "AKIAJJOUN2ESGFUQNI5A",
      secretAccessKey: "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",
      region: "us-east-1",
      endpoint: "runtime.lex.us-east-1.amazonaws.com"
    });

    var input = document.getElementById('lexInput').value;
    console.log(input);

    var lex = new AWS.LexRuntime();

    var params = {
      botAlias: 'demo', /* required */
      botName: 'Reginald', /* required */
      inputText: input, /* required */
      userId: 'Interface', /* required */
    };

    lex.postText(params, function(err, data) {
      if (err) {
        console.log(err, err.stack);
      } else {
        console.log(data);
      }

    });

  }

  retrieve() {

    var AWS = require('aws-sdk');

    AWS.config.update({
      accessKeyId: "AKIAJJOUN2ESGFUQNI5A",
      secretAccessKey: "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",
      region: "us-east-1",
      endpoint: "https://dynamodb.us-east-1.amazonaws.com"
    });

    var docClient = new AWS.DynamoDB.DocumentClient();
    var table = "LexHistory";

    docClient.scan({ TableName: table }, function(err, data) {
        if (err) {
            console.log(err);
        } else {
            data.Items.forEach(function(request) {

              var id = request.UUID
              var transcript = request.transcript
              var intent = request.intent
              var response = request.response

              rows.push({id, transcript, intent, response});

            });
        }
    })

    this.setState({rows: rows});

  }

  componentWillMount(){
    this.retrieve();
  }

  render() {

    return (
      <MuiThemeProvider theme={theme}>
   <div>
      <AppBar position="static" color="primary">
         <Toolbar>
            <Typography className="rms-title" variant="title" color="inherit">
               Reginald Management System
            </Typography>
         </Toolbar>
      </AppBar>
      <div className="container">
         <div className="facerec-flex">
            <div className="reg">
               <h2 className="register-h1">
                  Register New Face
               </h2>
               <div className="recognition">
                  <form className="recognition-form" onSubmit={this.handleSubmit.bind(this)}>
                     <TextField
                        id="formName"
                        label="Name"
                        margin="dense"
                        />
                     <div className="recognition-button">
                        <Button type="submit" variant="contained" color="primary">
                        Register
                        </Button>
                     </div>
                  </form>
                  <div className="recognition-button">
                     <Button onClick={this.handleClickOpen} variant="contained" color="primary">
                     Encode
                     </Button>
                  </div>
                  <Dialog
                     open={this.state.open}
                     onClose={this.handleClose}
                     aria-labelledby="alert-dialog-title"
                     aria-describedby="alert-dialog-description"
                     >
                     <DialogTitle id="alert-dialog-title">{"Begin Encoding Process?"}</DialogTitle>
                     <DialogContent>
                        <DialogContentText id="alert-dialog-description">
                           The facial recognition software will now encode the new photos across all exsiting faces.
                           Please be aware that this process may take some time.
                        </DialogContentText>
                     </DialogContent>
                     <DialogActions>
                        <Button onClick={this.handleClose} color="primary">
                        Disagree
                        </Button>
                        <Button onClick={this.handleEncode} variant="contained" color="primary" autoFocus>
                        Agree
                        </Button>
                     </DialogActions>
                  </Dialog>
               </div>
            </div>
            <div className="enable">

              <h2 className="register-h1">
                Toggle Recognition
              </h2>

              <div className="enable-inner">
                <div className="recognition-button">
                   <Button onClick={this.handleStartRec} variant="contained" color="primary">
                    START
                   </Button>
                </div>

                <div className="recognition-button">
                   <Button onClick={this.handleStopRec} variant="contained" color="primary">
                    STOP
                   </Button>
                </div>

              </div>

            </div>

            <div className="enable">

              <h2 className="register-h1">
                Query Lex
              </h2>

              <div className="recognition-form inForm">
                 <TextField
                    id="lexInput"
                    label="Query"
                    margin="dense"
                    />
                 <div className="recognition-button">
                    <Button onClick={this.handleInput.bind(this)}variant="contained" color="primary">
                    Send
                    </Button>
                 </div>
              </div>

            </div>

         </div>
         <h2 className="register-h1">
            Amazon Lex History
         </h2>
         <div className="databaseTable">
            <Paper>
               <Table>
                  <TableHead>
                     <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell>Intent</TableCell>
                        <TableCell>Transcript</TableCell>
                        <TableCell>Response</TableCell>
                     </TableRow>
                  </TableHead>
                  <TableBody id="tbd">

                    { rows.map(row => {
                      return (
                        <TableRow key={row.id}>
                          <TableCell component="th" scope="row">{row.id}</TableCell>
                          <TableCell>{row.intent}</TableCell>
                          <TableCell>{row.transcript}</TableCell>
                          <TableCell>{row.response}</TableCell>
                        </TableRow>
                      );
                    })}

                  </TableBody>
               </Table>
            </Paper>
         </div>
      </div>
   </div>
</MuiThemeProvider>
    );
  }
}

export default App;
