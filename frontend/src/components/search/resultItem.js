import { useState, useEffect } from 'react'
import { Card, Grid, Text, Group, Accordion, Badge } from '@mantine/core';

import RelatedPages from './relatedPages';

const ResultItem = (props) => {
    let result = props.item
    console.log(result)

    return (
        <>
            <Card
                withBorder
                radius="md"
                style={{
                    textAlign: "left",
                    marginBottom: "5px"
                }}
                shadow="lg"
                padding="xl"
            >

                <Card.Section
                    style={{
                        textAlign: "left",
                        marginBottom: "5px",
                        padding: "15px"
                    }}
                    component="a"
                    href={result.url}
                    target="_blank"
                >
                    <Group position="apart">
                        <Text weight={500} size="lg" >{result.Title} </Text>
                        <Text fz="xs" color="dimmed" fs="italic">Score: {result.Score}</Text>
                    </Group>

                    <Group position="apart">
                        <Text fz="xs" color="dimmed" fs="italic">{result.url}</Text>
                        <Text fz="xs" color="dimmed" fs="italic">Page Size: {result["Size of the Page"]} Byte</Text>
                        <Text fz="xs" color="dimmed" fs="italic">Last Modified: {result["Last Modified Date"]}</Text>

                    </Group>

                </Card.Section>
                <Badge size="lg" radius="xs" color="gray">Top 5 Term Frequency</Badge>
                {/* <Text mt="xs" color="dimmed" size="md" style={{ paddingBottom: 5 }}>
                    Top 5 Term Frequency<br />
                </Text> */}
                <Group style={{ margin: 10 }}>
                    {result["Most Frequent Items"].map((item, index) => {
                        return (
                            <Badge color="gray" size="lg" variant="outline">
                                {item.Item}: {item.Frequency}
                            </Badge>
                        )
                    })}
                </Group>

                <Grid >
                    <Grid.Col span={6}>
                        <Accordion >
                            <Accordion.Item variant="separated" value='child'>
                                <Accordion.Control style={{ padding: 5 }} >
                                    <Text mt="xs" color="dimmed" >
                                        Child Pages({result["Child Link"].length})
                                    </Text>
                                </Accordion.Control>
                                <Accordion.Panel>
                                    <RelatedPages pages={result["Child Link"]} />
                                </Accordion.Panel>
                            </Accordion.Item>
                        </Accordion>
                    </Grid.Col>
                    <Grid.Col span={6}>
                        <Accordion >
                            <Accordion.Item value="parent">
                                <Accordion.Control style={{ padding: 5 }} >
                                    <Text mt="xs" color="dimmed" >
                                        Parent Pages({result["Parent Link"].length})
                                    </Text>
                                </Accordion.Control>
                                <Accordion.Panel>
                                    <RelatedPages pages={result["Parent Link"]} />
                                </Accordion.Panel>
                            </Accordion.Item>
                        </Accordion>
                    </Grid.Col>
                </Grid>

            </Card>


        </>
    )
}

export default ResultItem;