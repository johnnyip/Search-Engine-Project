import { useState, useEffect } from 'react'
import { TextInput, Button, Group } from '@mantine/core';
import { IconSend, IconTrash } from '@tabler/icons';

import IndexingInfo from './indexingInfo';

import { checkIndexStat, startCrawl, removeCrawlContent } from '../../functions/crawl'

const Indexing = () => {
    const [url, setUrl] = useState('https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm')
    const [loading, setLoading] = useState(false)
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
                    disabled={indexStat.totalPageCrawled === undefined && indexStat.totalPageCrawled === 0}
                    onClick={async () => {
                        setLoading(true)
                        let stat = await removeCrawlContent()
                        setIndexStat(stat)
                        setLoading(false)
                    }}
                    leftIcon={<IconTrash size="1rem" />}>
                    Remove All Indexing
                </Button>

                <Button
                    loading={loading}
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
                    leftIcon={<IconSend size={20} />}>
                    {(loading) ? `Crawling and Indexing...(${timeElapsed}s)` : "Start Crawl and Indexing"}
                </Button>

            </Group>
            <IndexingInfo indexStat={indexStat} />
        </div>
    )


}


export default Indexing;