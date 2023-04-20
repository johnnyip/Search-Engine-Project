import { useState, useEffect } from 'react'
import { Card, Grid, Text, Group, Accordion, Badge, Chip, Button } from '@mantine/core';
import { IconCheck } from '@tabler/icons-react';

import RelatedPages from './relatedPages';

const ResultItem = (props) => {
    let result = props.item
    let filterTerm = props.filterTerm
    let setFilterTerm = props.setFilterTerm
    let setShowFilter = props.setShowFilter

    return (
        <Card
            withBorder
            radius="md"
            style={{
                textAlign: "left",
                marginBottom: "5px",
                padding: 20,
                marginTop: 20
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
            <Badge size="lg" radius="xs" color="gray">Top 5 Term Frequency In Document</Badge>
            {/* <Text mt="xs" color="dimmed" size="md" style={{ paddingBottom: 5 }}>
                    Top 5 Term Frequency<br />
                </Text> */}
            <Group style={{ margin: 10 }}>
                {result["Most Frequent Items"].map((item, index) => {
                    return (
                        <Button
                            // style={{paddingLeft:5, paddingRight:5, paddingBottom:5, paddingTop:5}}
                            radius="sm"
                            key={index}
                            compact
                            multiple={false}
                            leftIcon={(filterTerm === item.Item) ? <IconCheck size={19} /> : null}
                            onClick={() => {
                                if (filterTerm === item.Item) {
                                    setFilterTerm("")
                                } else {
                                    setFilterTerm(item.Item)
                                    setShowFilter(true)
                                }
                            }}
                            color={filterTerm === item.Item ? "blue" : "gray"}
                            variant={filterTerm === item.Item ? "filled" : "outline"}>
                            {item.Item}: {item.Frequency}
                        </Button>
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

        </Card >


    )
}

export default ResultItem;