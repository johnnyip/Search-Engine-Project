import { useState, useEffect } from 'react'
import { Button, Group, TextInput, Grid } from '@mantine/core';
import { IconX } from '@tabler/icons';

import HistoryItem from './historyItem'
import { getHistoryToken } from '../../functions/cookie'
import { saveRedis, getRedis } from '../../functions/redis'

const History = (props) => {
    let opened = props.opened
    let close = props.close
    let keyword = props.keyword
    let setKeyword = props.setKeyword
    let onSubmit = props.onSubmit

    const [history, setHistory] = useState([])

    useEffect(() => {
        const getSearchHistory = async () => {
            let historyToken = getHistoryToken()
            let history = await getRedis(historyToken)
            setHistory(history)
        }

        getSearchHistory()
    }, [opened])
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
            </Grid><br />
            <Button
                color='red'
                onClick={async () => {
                    let historyToken = getHistoryToken()
                    await saveRedis(historyToken, [])
                    setHistory([])
                }}>
                Remove All History
            </Button>
            <hr />

            {(history != []) ? [...history].map((item, index) => {
                return (
                    <HistoryItem
                        keyword={keyword}
                        setKeyword={setKeyword}
                        key={index}
                        item={item} />
                )
            }) : <>No History</>}
        </>
    )
}

export default History;