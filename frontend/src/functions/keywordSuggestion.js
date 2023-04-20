export class TrieNode {
    constructor() {
        this.children = {};
        this.isEndOfWord = false;
    }
}

export class Trie {
    constructor() {
        this.root = new TrieNode();
    }

    insert(word) {
        let currentNode = this.root;

        for (let i = 0; i < word.length; i++) {
            const char = word[i];

            if (!currentNode.children[char]) {
                currentNode.children[char] = new TrieNode();
            }

            currentNode = currentNode.children[char];
        }

        currentNode.isEndOfWord = true;
    }

    searchForSuggestions(prefix, limit = 5) {
        let currentNode = this.root;

        for (let char of prefix) {
            if (!currentNode.children[char]) {
                return [];
            }

            currentNode = currentNode.children[char];
        }

        return this.collectWords(currentNode, prefix, [], limit);
    }

    collectWords(node, prefix, words, limit) {
        if (words.length >= limit) {
            return words;
        }

        if (node.isEndOfWord) {
            words.push(prefix);
        }

        for (let char in node.children) {
            words = this.collectWords(node.children[char], prefix + char, words, limit);
        }

        return words;
    }
}
