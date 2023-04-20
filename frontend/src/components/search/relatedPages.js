import { useState, useEffect } from 'react'
import { ScrollArea, Box, Card, Text, Group } from '@mantine/core';

const RelatedPages = (props) => {
    let result = props.pages

    return (
        <>
            <ScrollArea >
                <Box >
                    {result.map((item, index) => {
                        // console.log(item)
                        return (
                            <Card
                                key={index}
                                withBorder
                                radius="md"
                                style={{
                                    textAlign: "left",
                                    marginBottom: "5px"
                                }}
                                shadow="lg"
                                padding="xl"
                                component="a"
                                href={item.url}
                                target="_blank"

                            >
                                <Text weight={500} size="lg" >{item.Title} </Text>
                                <Text fz="xs" color="dimmed" fs="italic">{item.url}</Text>

                            </Card>
                        )
                    })}
                </Box>
            </ScrollArea>

        </>
    )
}

export default RelatedPages;