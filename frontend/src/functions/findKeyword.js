export const findKeyword = (text, keywords, contextWords = 5) => {
    const snippets = [];
    const keywordRegex = new RegExp(`\\b(${keywords.join('|')})\\b`, 'gi');

    const getWords = (input, count, reverse = false) => {
        const words = input.split(' ');
        if (reverse) words.reverse();
        const result = words.slice(0, count).join(' ');
        return reverse ? result.split(' ').reverse().join(' ') : result;
    };

    let match;
    while ((match = keywordRegex.exec(text)) !== null) {
        const beforeText = text.slice(0, match.index).trim();
        const afterText = text.slice(match.index + match[0].length).trim();

        const beforeMatch = getWords(beforeText, contextWords, true);
        const afterMatch = getWords(afterText, contextWords);

        snippets.push([beforeMatch, match[0], afterMatch]);
    }

    return snippets;
};
