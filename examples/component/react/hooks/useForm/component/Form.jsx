import useForm from "../hook/useForm";

const Form = () => {
  const initialState = { email: "", password: "" };
  const [values, setValues] = useForm(initialState);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(values);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" name="email" onChange={setValues} />
      <input type="password" name="password" onChange={setValues} />
      <button type="submit">Submit</button>
    </form>
  );
};

export default Form;
