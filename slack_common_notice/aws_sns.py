from slack_common_notice.notice import Notice


def subscribe(event):
    notices = by_event(event)
    if not notices:
        return False
    for n in notices:
        n.send()
    return True


def by_event(event):
    if 'Records' not in event:
        return False
    notices = []
    for record in event['Records']:
        notices.append(by_record(record))
    return notices


def by_record(record):
    sns = record['Sns']
    con = {'title': sns['Subject'], 'text': sns['Message']}
    if 'MessageAttributes' in sns:
        attr = sns['MessageAttributes']
        if 'url' in attr:
            con['url'] = attr['url']['Value']
        if 'level' in attr:
            con['level'] = attr['level']['Value']
    return Notice(con)


if __name__ == '__main__':
    import unittest
    import json

    class NoticeTest(unittest.TestCase):
        def setUp(self):
            pass

        def test_init_by_records(self):
            event = '{"Records":[{"EventSource":"aws:sns","EventVersion":"1.0","EventSubscriptionArn":"arn:aws:sns:xxxx","Sns":{"Type":"Notification","MessageId":"xxxx","TopicArn":"arn:aws:sns:xxxx","Subject":"subjectbysns","Message":"msgbysns","Timestamp":"2022-03-05T22:57:07.775Z","SignatureVersion":"1","Signature":"xxx","SigningCertUrl":"https:/example.com","UnsubscribeUrl":"https:/example.com","MessageAttributes":{"level":{"Type":"String","Value":"alert"}}}},{"EventSource":"aws:sns","EventVersion":"1.0","EventSubscriptionArn":"arn:aws:sns:xxxx","Sns":{"Type":"Notification","MessageId":"xxxx","TopicArn":"arn:aws:sns:xxxx","Subject":"subjectbysns2","Message":"msgbysns2","Timestamp":"2022-03-05T22:57:07.775Z","SignatureVersion":"1","Signature":"xxx","SigningCertUrl":"https:/example.com","UnsubscribeUrl":"https:/example.com","MessageAttributes":{"url":{"Type":"String","Value":"slack.example.com"}}}}]}'
            notices = by_event(json.loads(event))
            self.assertEqual(2, len(notices))
            self.assertEqual('subjectbysns', notices[0].title)
            self.assertEqual('msgbysns', notices[0].text)
            self.assertIsNone(notices[0].url)
            self.assertEqual('alert', notices[0].level)
            self.assertEqual('subjectbysns2', notices[1].title)
            self.assertEqual('msgbysns2', notices[1].text)
            self.assertEqual('slack.example.com', notices[1].url)
            self.assertIsNone(notices[1].level)
    unittest.main()
