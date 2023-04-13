import { useState, useEffect } from 'react'
import { Button, Group, TextInput, Grid, Accordion } from '@mantine/core';
import { IconPlus } from '@tabler/icons';

import SearchResult from './searchResult';

import { formatDate } from '../../functions/date'

const HistoryItem = (props) => {
    let item = props.item
    let keyword = props.keyword
    let setKeyword = props.setKeyword

    // console.log(item) 
    return (
        <>
            <Grid grow style={{ marginLeft: "5%", marginRight: "5%", textAlign: "left" }}>
                <Grid.Col span={8} style={{}}>
                    <b>Keyword:</b> {item.data.keyword}
                </Grid.Col>
                <Grid.Col span={2}>
                    <Button
                        onClick={() => {
                            setKeyword(`${keyword} ${item.data.keyword}`)
                        }}
                        leftIcon={<IconPlus size={20} />}>
                        Append keyword
                    </Button>
                </Grid.Col>


            </Grid>

            <Grid grow style={{ marginLeft: "5%", marginRight: "5%", textAlign: "left" }}>
                <Grid.Col span={2}>
                    <b>Algorithm: </b>{item.algo}
                </Grid.Col>

                <Grid.Col span={4}>
                    <b>Date: </b>{item.queryDate}
                </Grid.Col>
            </Grid>

            <div>
                <Accordion style={{ marginLeft: "5%", marginRight: "5%", textAlign: "left" }}>
                    <Accordion.Item value="result">
                        <Accordion.Control>Search Result</Accordion.Control>
                        <Accordion.Panel>

                            <SearchResult variant="filled" result={item} />

                        </Accordion.Panel>
                    </Accordion.Item>
                </Accordion>

            </div>

            <hr />
        </>
    )
}

export default HistoryItem;