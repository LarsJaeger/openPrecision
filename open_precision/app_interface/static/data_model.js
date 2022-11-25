import { Data } from 'dataclass';

class DataModelBase extends Data{
    *to_json() {
        return JSON.stringify(this);
    }
}
class Action extends DataModelBase {
    id;
    initiator;
    function_identifier;
    args;
    kw_args;
    action_response;
}