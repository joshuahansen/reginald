import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import MuiThemeProvider from '@material-ui/core/styles/MuiThemeProvider';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { createMuiTheme } from '@material-ui/core/styles';

const muiTheme = createMuiTheme ({
    palette: {
        "primary1Color": "#e60228",
        "primary2Color": "#d32f2f",
        "accent1Color": "#448aff"
    },
});

class App extends Component {

  render() {
    return (

        <div>
          <AppBar position="static" color="default">
            <Toolbar>
              <Typography variant="title" color="inherit">
                Reginald Management System
              </Typography>
            </Toolbar>
          </AppBar>
        </div>

    );
  }
}

export default App;
