import { useState, useEffect } from 'react'
import { Card, Image, Text, Group } from '@mantine/core';

const ResultItem = (props) => {
    let result = props.item
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
                component="a"
                href={result.url}
                target="_blank"
            >


                <Group position="apart">
                    <Text weight={500} size="lg" >
                        Fake Result Title
                    </Text>

                    <Text fz="xs" color="dimmed" fs="italic">
                        Score: {result.score}
                    </Text>
                </Group>

                <Text fz="xs" color="dimmed" fs="italic">
                    {result.url}
                </Text>


                <Text mt="xs" color="dimmed" size="md">
                    Text with keywords <b>bolded</b>
                </Text>
            </Card>


        </>
    )
}

export default ResultItem;