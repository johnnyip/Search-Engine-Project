import { useState, useEffect } from 'react'
import { Badge, Table } from '@mantine/core';
import { IconSend } from '@tabler/icons-react';


const IndexingInfo = (props) => {
    const indexStat = props.indexStat

    const duration = indexStat.duration !== undefined ? indexStat.duration : 0
    const totalPageCrawled = indexStat.totalPageCrawled !== undefined ? indexStat.totalPageCrawled : 0
    const totalTerms = indexStat.totalTerms !== undefined ? indexStat.totalTerms : 0
    const totalStems = indexStat.totalStems !== undefined ? indexStat.totalStems : 0

    return (
        <>
            <hr style={{ marginTop: 50 }} />
            <h3>Indexing Information</h3>

            <div style={{ marginLeft: "30%", marginRight: "30%" }}>
                <Table
                    striped highlightOnHover withColumnBorders>

                    <tbody>
                        <tr>
                            <th>Time Used For Crawling Indexing</th>
                            <th>{duration}</th>
                        </tr>
                        <tr>
                            <th>Total Document Indexed</th>
                            <th>{totalPageCrawled}</th>
                        </tr>
                        <tr>
                            <th>Total Terms</th>
                            <th>{totalTerms}</th>
                        </tr>
                        <tr>
                            <th>Total Stemmed Words</th>
                            <th>{totalStems}</th>
                        </tr>
                    </tbody>
                </Table>

            </div>
        </>
    )
}


export default IndexingInfo;