import useCopyToClipboard from "../hook/useCopyToClipboard";

const TextCopy = (props) => {
  const [copied, copy] = useCopyToClipboard("Lorem ipsum");
  return (
    <div>
      <button onClick={copy}>Click to copy</button>
      <span>{copied && "Copied!"}</span>
    </div>
  );
};

export default TextCopy;
