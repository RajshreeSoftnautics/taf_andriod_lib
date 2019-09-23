###############################################################
# Library to send email with attachment to one or more users
###############################################################

import os
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class sendemail():

    def sendEmail(self, protocol, serverName, portNum, subject, fromAddr,
                  password, toAddr, ccAddr, bccAddr, body, attachmentList):
        """
        Method to send email with attachment to one or more users.
        Args:
        protocol: SSL or TLS protocol
        serverName: smtp server name
        portNum: port number use for smtp
        subject: Email subject
        fromAddr: From email address
        password: From email address password
        toAddr: List of to email address
        ccAddr: List of cc email address
        bccAddr: List of bcc email address
        body: Email body string
        attachment: List of attachment
        """
        try:
            message = MIMEMultipart("alternative", None, [MIMEText(body)])
            message["From"] = fromAddr
            message["Subject"] = str(subject)
            message["To"] = ", ".join(toAddr)
            message["CC"] = ", ".join(ccAddr)
            message["BCC"] = ", ".join(bccAddr)

            for attachment in attachmentList:
                if os.path.exists(attachment):
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(open(attachment, "rb").read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", 'attachment;\
                                    filename="%s"'
                                    % os.path.basename(attachment))
                    message.attach(part)
                else:
                    print("Attachment Missing : ", attachment)
                    return False

            text = message.as_string()

            if protocol.lower() == "tls":
                server = smtplib.SMTP(serverName, int(portNum))
                server.starttls()
                server.login(fromAddr, password)
                server.sendmail(fromAddr, ", ".join(toAddr), text)
                server.quit()
            elif protocol.lower() == "ssl":
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(serverName, int(portNum),
                                      context=context) as server:
                    server.login(fromAddr, password)
                    server.sendmail(fromAddr, ", ".join(toAddr), text)
                    server.quit()

            print("Email Sent")

        except Exception as error:
            print("Exception while sending email, Please provide correct\
data in config file")
            return (False, error)

        return True
