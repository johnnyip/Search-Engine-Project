import { useState, useEffect } from 'react'
import { TextInput, Button, Group } from '@mantine/core';
import { IconSend, IconTrash } from '@tabler/icons-react';

import IndexingInfo from './indexingInfo';

import { checkIndexStat, startCrawl, removeCrawlContent } from '../../functions/crawl'
import { dbUpdate } from '../../functions/query'

const Indexing = () => {
    const [url, setUrl] = useState('https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm')
    const [loading, setLoading] = useState(false)
    const [loading2, setLoading2] = useState(false)
    const [indexStat, setIndexStat] = useState({})
    const [timeElapsed, setTimeElapsed] = useState(0)

    const startTimer = (stopCallback) => {
        const duration = setInterval(() => {
            setTimeElapsed(timeElapsed => timeElapsed + 1);
        }, 1000);

        // Call stopCallback to stop the timer
        const stopTimer = () => {
            clearInterval(duration);
            stopCallback();
        };

        // Return stopTimer function
        return stopTimer;
    };

    const loadData = async () => {
        const indexStat_ = await checkIndexStat()
        setIndexStat(indexStat_)
    }

    useEffect(() => {
        // console.log("Indexing page loaded")
        loadData()
    }, [])


    return (
        <div className='moreSpace'>
            <h3>Enter the URL to be crawled</h3>
            <Button
                color="gray"
                onClick={() => setUrl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm")}
                style={{ margin: 10 }}>
                Load sample data URL
            </Button>

            <TextInput
                value={url}
                onChange={(event) => setUrl(event.currentTarget.value)}
                disabled
                style={{ marginLeft: "20%", marginRight: "20%" }}
            /><br />

            <Group position="center">
                <Button
                    color="red"
                    disabled={indexStat.totalPageCrawled === undefined && indexStat.totalPageCrawled === 0 || loading || loading2}
                    onClick={async () => {
                        setLoading(true)
                        let stat = await removeCrawlContent()
                        setIndexStat(stat)
                        setLoading(false)
                    }}
                    leftIcon={<IconTrash height={20} width={20} />}>
                    Remove All Indexing
                </Button>

                <Button
                    loading={loading}
                    disabled={loading2}
                    onClick={async () => {
                        setLoading(true)
                        let timerStopped = false;
                        const stopTimerCallback = () => {
                            timerStopped = true;
                            setLoading(false);
                        };
                        const stopTimer = startTimer(stopTimerCallback);
                        let stat = await startCrawl(url);
                        setIndexStat(stat)


                        // Stop the timer only if it's still running
                        if (!timerStopped) {
                            stopTimer();
                        }
                    }}
                    leftIcon={<IconSend height={20} width={20} />}>
                    {(loading) ? `Crawling and Indexing...(${timeElapsed}s)` : "Start Crawl and Indexing (Java)"}
                </Button>

                <Button
                    loading={loading2}
                    disabled={loading}
                    onClick={async () => {
                        setLoading2(true)
                        let timerStopped = false;
                        const stopTimerCallback = () => {
                            timerStopped = true;
                            setLoading2(false);
                        };
                        const stopTimer = startTimer(stopTimerCallback);
                        await dbUpdate();


                        // Stop the timer only if it's still running
                        if (!timerStopped) {
                            stopTimer();
                        }
                    }}
                    leftIcon={<IconSend height={20} width={20}/>}>
                    {(loading2) ? `Sync Database...(${timeElapsed}s)` : "Sync Database (Python)"}
                </Button>

            </Group>
            <IndexingInfo indexStat={indexStat} />
        </div>
    )


}


export default Indexing;