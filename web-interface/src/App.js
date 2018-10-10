import React, { Component } from 'react';
import './App.css';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Drawer from '@material-ui/core/Drawer';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';


const theme = createMuiTheme ({
    palette: {
        primary: { main: '#e60228'},
        secondary: { main: '#448aff'},
    },
});

class App extends Component {

  state = {
    open: false,
  }

  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.retrieve = this.retrieve.bind(this);
  }

  toggleDrawer = (side, open) => () => {
    this.setState({
      [side]: open,
    });
  };

  handleSubmit() {

    console.log("Test");

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

    console.log("Scanning LexHistory table.");

    docClient.scan({ TableName: table }, function(err, data) {
        if (err) {
            console.log(err);
        } else {
            console.log("Success");
            console.log(data);
            data.Items.forEach(function(request) {
              console.log(
                request.UUID + ": ",
                request.transcript, " - ", request.response
              );

              var id = request.UUID
              var transcript = request.transcript
              var intent = request.intent
              var response = request.response

              const tbd = document.getElementById('tbd');

              const row = document.createElement('TableRow');

              const idCell = document.createElement('TableCell');
              idCell.textContent = id;
              const tsCell = document.createElement('TableCell');
              tsCell.textContent = transcript;
              const inCell = document.createElement('TableCell');
              inCell.textContent = intent;
              const resCell = document.createElement('TableCell');
              resCell.textContent = response;

              tbd.appendChild(row);
              row.appendChild(idCell);
              row.appendChild(tsCell);
              row.appendChild(inCell);
              row.appendChild(resCell);

            });
        }
    })

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
              <IconButton onClick={this.toggleDrawer('open', true)} color="inherit" aria-label="Menu">
                <MenuIcon />
              </IconButton>
              <Drawer className="drawer" open={this.state.open} onClose={this.toggleDrawer('open', false)}>
                <div
                  tabIndex={0}
                  role="button"
                  onClick={this.toggleDrawer('open', false)}
                  onKeyDown={this.toggleDrawer('open', false)}
                >

                  <div>
                    <MenuItem>Menu Item 1</MenuItem>
                    <MenuItem>Menu Item 2</MenuItem>
                    <MenuItem>Menu Item 3</MenuItem>
                    <MenuItem>Menu Item 4</MenuItem>
                  </div>
                </div>
              </Drawer>
              <Typography variant="title" color="inherit">
                Reginald Management System
              </Typography>
            </Toolbar>
          </AppBar>

          <div className="container">
          <h2 className="register-h1">
            Register New Face
          </h2>

          <div className="recognition">
            <form className="recognition-form" onSubmit={this.handleSubmit.bind(this)}>
              <TextField
                id="standard-dense"
                label="Name"
                margin="dense"
              />
              <div className="recognition-button">
                <Button type="submit" variant="contained" color="primary">
                  Register
                </Button>
              </div>
            </form>
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

                <TableRow>
                  <TableCell component="th" scope="row">1</TableCell>
                  <TableCell>Get weather for Melbourne</TableCell>
                  <TableCell>What is the weather for melbourne?</TableCell>
                  <TableCell>It is currently 26 Degrees Celcius</TableCell>
                </TableRow>

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
