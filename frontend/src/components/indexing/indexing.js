import {useState, useEffect} from 'react'
import {TextInput, Button, Group} from '@mantine/core';
import {IconSend, IconTrash} from '@tabler/icons';

import IndexingInfo from './indexingInfo';

import {checkCrawlPageCount, startCrawl, removeCrawlContent} from '../../functions/crawl'

const Indexing = () => {
    const [url, setUrl] = useState('https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm')
    const [loading, setLoading] = useState(false)
    const [pageCount, setPageCount] = useState(0)
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
        const countResult = await checkCrawlPageCount()
        setPageCount(countResult)
    }

    useEffect(() => {
        console.log("Indexing page loaded")
        loadData()
    }, [])


    return (
        <div className='moreSpace'>
            <h3>Enter the URL to be crawled</h3>
            <Button
                color="gray"
                onClick={() => setUrl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm")}
                style={{margin: 10}}>
                Load sample data URL
            </Button>

            <TextInput
                value={url}
                onChange={(event) => setUrl(event.currentTarget.value)}
                style={{marginLeft: "20%", marginRight: "20%"}}
            /><br/>

            <Group position="center">
                <Button
                    color="red"
                    disabled={pageCount === 0}
                    onClick={async () => {
                        setLoading(true)
                        await removeCrawlContent()
                        const countResult = await checkCrawlPageCount()
                        setPageCount(countResult)
                        setLoading(false)
                    }}
                    leftIcon={<IconTrash size="1rem"/>}>
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
                        await startCrawl(url);
                        setPageCount(await checkCrawlPageCount())


                        // Stop the timer only if it's still running
                        if (!timerStopped) {
                            stopTimer();
                        }
                    }}
                    leftIcon={<IconSend size="1rem"/>}>
                    {(loading) ? `Crawling and Indexing...(${timeElapsed}s)` : "Start Crawl and Indexing"}
                </Button>

            </Group>
            <IndexingInfo pageCount={pageCount}/>
        </div>
    )


}


export default Indexing;