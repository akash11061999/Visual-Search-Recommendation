import React from 'react';
import { Route, Switch } from 'react-router';
import Home from './Home';
import SearchResult from './SearchResult';

export default function Routes(){
    return(
        <div>
            <Switch>
                <Route exact path="/home" component={Home}/>
                <Route exact path="/searchResult" component={SearchResult}/>
                <Route exact path="/" component={Home} />
            </Switch>
        </div>
    )
}