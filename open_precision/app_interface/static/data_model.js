import { Data } from "https://unpkg.com/dataclass@2?module";

class DataModelBase extends Data{
    *to_json() {
        return JSON.stringify(this);
    }
}
export class Action extends DataModelBase {
    id;
    initiator;
    function_identifier;
    args;
    kw_args;
    action_response;
}