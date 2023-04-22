import  { SSMLParser }  from "./libraries/Biku/ssml parser.js"

function translateShorthand(text) {
    let parser = new SSMLParser(text)
    parser.initialize(text)
    let parsed = parser.parse(text)
    return parsed
}

var arg = process.argv.slice(2)

var farg = String(arg)
console.log(translateShorthand(farg));
