import { Alert } from "flowbite-react";
import { Dispatch, SetStateAction } from "react";

const AlertError = ({ error, setError }: {error: string, setError: Dispatch<SetStateAction<string>>}) => {
    return (
        <div className="absolute w-full">
            {error && <Alert color="failure" onDismiss={() => setError('')} withBorderAccent>
                <span className="font-medium">{error}</span>
            </Alert>}
        </div>
    );
}

export default AlertError;