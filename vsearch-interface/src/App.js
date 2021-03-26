import React from 'react';
import { BrowserRouter} from "react-router-dom";
import createMuiTheme from "@material-ui/core/styles/createMuiTheme";
import { ThemeProvider as MuiThemeProvider } from '@material-ui/core/styles';
import blue from "@material-ui/core/colors/blue";
import Routes from './components/Routes';


const outerTheme = createMuiTheme({
  palette: {
      primary: {
          main: blue[400],
      },
      secondary: {
          main: blue[400],
      },
  },
  overrides:{

  }
});


function App() {

  return (
    <BrowserRouter>
          {/* <MuiThemeProvider theme={outerTheme}> */}
              <Routes/>
          {/* </MuiThemeProvider> */}
      </BrowserRouter>
  );
}

export default App;
