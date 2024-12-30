import { Alert, Spinner } from "flowbite-react";

const AlertSend = ({ title } : {title: string}) => {
    return (
        <Alert color="info">
            <span className="w-screen px-20 font-medium flex flex-row justify-between items-center">
                {title}
                <Spinner size="sm" className="self-end" />
            </span>
        </Alert>
    );
}

export default AlertSend;