import { useState } from 'react'
import './components/UI/AlertError'
import AlertError from './components/UI/AlertError.tsx';
import { Alert } from "flowbite-react";

function App() {
  const [error, setError] = useState<string>('some error');
  return (
    <>
    <Alert color="info">
      <span>Message</span>
    </Alert>
    </>
  )
}

export default App
