import { useState, useEffect } from 'react'
import { Button, Group, TextInput, Grid } from '@mantine/core';
import { IconX } from '@tabler/icons';

import HistoryItem from './historyItem'
import { saveHistory, getHistory, removeHistory } from '../../functions/cookie'

const History = (props) => {
    let close = props.close
    let keyword = props.keyword
    let setKeyword = props.setKeyword
    let onSubmit = props.onSubmit

    const [cookie, setCookie] = useState("")

    useEffect(() => {
        let history = getHistory()
        setCookie(history)
    }, [])
    return (
        <>
            <div>Current Search</div>
            <Grid style={{ marginLeft: "15%", marginRight: "0%" }}>

                <Grid.Col span={8}>
                    <TextInput
                        value={keyword}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                onSubmit();
                            }
                        }}
                        onChange={(event) => setKeyword(event.currentTarget.value)}
                    />
                </Grid.Col>

                <Grid.Col span={4}>
                    <Group position="left" spacing="xs">
                        <Button
                            onClick={() => {
                                setKeyword("")
                            }}
                            leftIcon={<IconX size="15" />}>
                            Clear
                        </Button>
                        <Button
                            disabled={keyword.length === 0}
                            style={{ textAlign: "left" }}
                            onClick={async (e) => {
                                e.preventDefault();
                                close()
                                await onSubmit()
                            }}>
                            Search
                        </Button>

                    </Group>
                </Grid.Col>
            </Grid>
            <Button
                color='red'
                onClick={() => {
                    removeHistory()
                }}>
                Remove History
            </Button>
            <hr />

            {[...cookie].map((item, index) => {
                return (
                    <HistoryItem
                        keyword={keyword}
                        setKeyword={setKeyword}
                        key={index}
                        item={item} />
                )
            })}
        </>
    )
}

export default History;