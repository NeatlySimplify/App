module default {

    type Admin {
        required name: str;
        required email: str;
        required password: str;
    }

    type Client {
        user: User;
        required timestamp: datetime {
            default := datetime_of_statement();
        };
        required email: str {
            delegated constraint exclusive;
        };
        name: str;
        sex: str;
        relationship: str;
        details: str;
        category: str;
        birth: datetime;
        city: str;
        state: str;
        phone: json;
        address: json;

        trigger log_update after update for each when ( <json>__old__ {*} != <json>__new__ {*}
        ) do (
            insert Auditable {
                user := __old__.user.id,
                id_objeto := __old__.id,
                action := "update",
                details := to_json(
                    '{' ++
                    '"before": ' ++ <str><json>__old__{*} ++ ',' ++
                    '"after": ' ++ <str><json>__new__{*} ++
                    '}'
                ),
            }
        );

        trigger log_insert after insert for each do (
            insert Auditable {
                user := __new__.user.id,
                id_objeto := __new__.id,
                action := "insert",
                details := <json>__new__{*}
            }
        );

        trigger log_delete after delete for each do (
            insert Auditable {
                user := __old__.user.id,
                id_objeto := __old__.id,
                action := "delete",
                details := <json>__old__{*}
            }
        );
    }

    type Service {
        user: User;
        folder: str;
        id_Service: str;
        status: bool;
        value: float32;
        category: str;
        details: str;
        custom: json;
        multi clients: Client {
            on source delete delete target if orphan;
        };
        multi event: Scheduler {
            on source delete delete target;
            on target delete allow;
        };
        action: Action {
            on source delete delete target;
            on target delete allow;
        };

        trigger log_update after update for each when (
            <json>__old__{*} != <json>__new__{*}
        ) do (
            insert Auditable {
                user := __old__.user.id,
                id_objeto := __old__.id,
                action := "update",
                details := to_json(
                    '{' ++
                    '"before": ' ++ <str><json>__old__{*} ++ ',' ++
                    '"after": ' ++ <str><json>__new__{*} ++
                    '}'
                )
            }
        );

        trigger log_insert after insert for each do (
            insert Auditable {
                user := __new__.user.id,
                id_objeto := __new__.id,
                action := "insert",
                details := <json>__new__{*}
            }
        );

        trigger log_delete after delete for each do (
            insert Auditable {
                user := __old__.user.id,
                id_objeto := __old__.id,
                action := "delete",
                details := <json>__old__{*},
            }
        );
    }

    type Templates {
        user: User;
        name: str;
        category: str;
        fields: json;
    }

    type Auditable {
        required timestamp: datetime {
            default := datetime_of_statement();
        };
        id_objeto: uuid;
        user: uuid;
        action: str;
        details: json;
    }

    type Scheduler {
        user: User;
        origin: uuid;
        name: str;
        status: bool {
            default:= false;
        };
        end_time: datetime;
        effective: datetime;
        cycle: str;
        details: str;
        tag_type: str;
        auto_change_status: bool {
            default:= false;
        };
    }

    type BankAccount {
        bankName: str;
        agency: str;
        accountNumber: str;
        balance: float32;
        accountType: str;
    }

    type User {
        required name: str;
        required email: str;
        required password: str;
        isActive: bool{
            default := false;
        };
        lastActiveDate: datetime;
        multi account: BankAccount {
            on target delete allow;
            on source delete delete target;
        };

        # Usando backlinks para selecionar de modo dinâmico todas as entradas com o uuid do usuário
        # quando o usuário é deletado, todas as entradas ligadas ao usuário são excluidas.
        multi service := (.<user[is Service]);
        multi client := (.<user[is Client]);
        multi actions := (.<user[is Action]);
        multi event := (.<user[is Scheduler]);
        multi templates := (.<user[is Templates]);

        trigger log_update after update for each when (
            <json>__old__ {*} != <json>__new__ {*}
        ) do (
            insert Auditable {
                user := __old__.id,
                id_objeto := __old__.id,
                action := "update",
                details := to_json('{' ++ '"before": ' ++ <str><json>__old__{*} ++ ',' ++ '"after": ' ++ <str><json>__new__{*} ++'}')
            }
        );

        trigger log_insert after insert for each do (
            insert Auditable {
                user := __new__.id,
                id_objeto := __new__.id,
                action := "insert",
                details := <json>__new__ {*}
            }
        );

        trigger log_delete after delete for each do (  
            insert Auditable {
                user := __old__.id,
                id_objeto := __old__.id,
                action := "delete",
                details := <json>__old__ {*}
            }
        );
        trigger link_delete after delete for each do (
            delete (select User.<user)
        );
    }

    type Action {
        user: User;
        name: str;
        value: float32;
        installment: int16;
        cycle: str;
        effective: bool {
            default := false;
        };
        category: str;
        subcategory: str;
        account: BankAccount;
        multi payment: Payment{
            on source delete delete target;
            on target delete allow;
        };

        trigger log_update after update for each when (
            <json>__old__ {*} != <json>__new__ {*}
        ) do (
            insert Auditable {
                user := __old__.user.id,
                id_objeto := __old__.id,
                action := "update",
                details := to_json(
                    '{' ++
                    '"before": ' ++ <str><json>__old__{*} ++ ',' ++
                    '"after": ' ++ <str><json>__new__{*} ++
                    '}'
                )
            }
        );

        trigger log_insert after insert for each do (
            insert Auditable {
                user := __new__.user.id,
                id_objeto := __new__.id,
                action := "insert",
                details := <json>__new__ {*}
            }
        );

        trigger log_delete after delete for each do (
            insert Auditable {
                user := __old__.user.id,
                id_objeto := __old__.id,
                action := "delete",
                details := <json>__old__ {*}
            }
        );
    }

    type Payment {
        user: User;
        action: Action;
        value: float32;
        paymentDate: datetime;
        isDue: datetime;
        status: bool{
            default:= false;
        };
        part: int16;
        event: Scheduler {
            on source delete delete target;
        }

        # Updates balance on action.account.balance when insert Payment.
        trigger update_balance_on_insert after insert for each when (
            __new__.status = true
        ) do (
            update BankAccount filter .id = __new__.action.account.id set {
                balance := .balance + __new__.value
            }
        );

        # Updates from balance on action.account.balance when delete Payment.
        trigger update_balance_on_delete after delete for each when (
            __old__.status = true
        ) do (
            update BankAccount filter .id = __old__.action.account.id set {
                balance := .balance - __old__.value
            }
        );

        # Updates from balance on action.account.balance when update Payment.
        trigger update_balance_on_update after update for each when (
            (__old__.status = true or __new__.status = true) and (
                __old__.value != __new__.value or
                __old__.action.account != __new__.action.account or
                __old__.status != __new__.status
            )
        ) do (
            with
                update_account := (update BankAccount filter .id in {
                    __old__.action.account.id, __new__.action.account.id} set {
                    balance := (.balance - __old__.value) if .id = __old__.action.account.id
                    else (.balance + __new__.value) if .id = __new__.action.account.id
                    else .balance}),
                new_effective := (update BankAccount filter .id = __old__.action.account.id set {
                    balance := .balance + __old__.value}),

                not_effective := (update BankAccount filter .id = __old__.action.account.id set {
                        balance := .balance - __old__.value})

            select update_account if (__old__.value != __new__.value or __old__.action.account != __new__.action.account)
            else new_effective if __new__.status = true
            else not_effective
        );

        # Updates Action.effective to TRUE if all instances associated to Action.payment has status equal to TRUE. The query is executed on each insert or update on Payment.
        trigger update_status_action after update, insert for each when (__new__.status = true) do (
            with action_linked:= (select Action filter .id = __new__.action.id),
            not_effective:= (select Payment filter .action = __new__.action and .status = false),
            update Action filter .id = action_linked.id set {effective:= (select not exists not_effective)}
        );

        # Insert Payment.event.
        trigger create_event after insert for each do (
            with data := ( insert Scheduler {
                user:= __new__.user,
                origin:= __new__.action.id,
                name:= __new__.action.name,
                status:= __new__.status,
                end_time:= __new__.isDue,
                effective:= __new__.paymentDate,
                cycle:= "Unique",
                tag_type:= "Action",
                }
            )
            update Payment filter .id = __new__.id set {
                event := data
            }
        );
        
        # Updates Payment.event.
        trigger update_event after update for each do (
            update __old__.event set {
                name:= __new__.action.name,
                status:= __new__.status,
                end_time:= __new__.isDue,
                effective:= __new__.paymentDate,
            }
        )
    }
}
