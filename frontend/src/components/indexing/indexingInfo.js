import { useState, useEffect } from 'react'
import { Badge, Table } from '@mantine/core';
import { IconSend } from '@tabler/icons';

const IndexingInfo = () => {

    return (
        <>
            <hr style={{ marginTop: 50 }} />
            <h3>Indexing Information</h3>

            <div style={{ marginLeft: "30%", marginRight: "30%" }}>
                <Table
                    striped highlightOnHover withColumnBorders>

                    <tbody>
                        <tr>
                            <th>Total Document Indexed</th>
                            <th>2</th>
                        </tr>
                        <tr>
                            <th>Total Keywords Indexed</th>
                            <th>2</th>
                        </tr>
                        <tr>
                            <th>Time Used For Crawling</th>
                            <th>50 Seconds</th>
                        </tr>
                        <tr>
                            <th>Time Used For Indexing</th>
                            <th>50 Seconds</th>
                        </tr>
                    </tbody>
                </Table>

            </div>
        </>
    )
}


export default IndexingInfo;