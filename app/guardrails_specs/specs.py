rail_str = """
<rail version="0.1">

<output>
    <list name="transaction_list">
        <object name="transaction_info">
            <date name="transaction_date" date-format="%Y-%m-%d" />
            <string name="transaction_description"/>
            <float name="debit"/>
            <float name="credit"/>
            <float name="balance"/>
        </object>
    </list>
</output>

<prompt>

I will present you a bank statement that has the following elements:

- transaction_date: The date of the transaction
- transaction_description: The description of the transaction
- debit: The amount of money debited from the account
- credit: The amount of money credited to the account
- balance: The balance of the account after the transaction

I want to extract this information separately for each transaction in the bank statement below:

{{transaction_string}}
@complete_json_suffix_v2</prompt>


</rail>
"""
