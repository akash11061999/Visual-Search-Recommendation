import React, { Component } from 'react';
import Navbar from './NavBar'
import ItemCard from './ItemCard'
import { Container } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import SearchResult from './SearchResult';


export default class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isQueryImageUploaded: false,
            queryImg: {}
        }
    }

    render() {
        if (this.state.isQueryImageUploaded) {
            <React.Fragment>
                <SearchResult/>
            </React.Fragment>
        }
        else {
            return (
                <React.Fragment>
                    <Container
                        maxWidth="lg"
                        style={{
                            position: "relative",
                            marginTop: "75px",
                            //backgroundColor: '#ECF0F1'
                        }}>
                        <Navbar props={this.props}/>
                        <Grid container spacing={3}>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                            <Grid item xs={4}>
                                <ItemCard />
                            </Grid>
                        </Grid>

                    </Container>
                </React.Fragment>
            )
        }

    }
}