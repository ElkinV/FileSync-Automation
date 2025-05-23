import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import logging
import os
from main import main
from config import LOG_SETTINGS

# Configure logging
log_dir = os.path.dirname(os.path.abspath(LOG_SETTINGS['log_file']))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=LOG_SETTINGS['log_file'],
    level=getattr(logging, LOG_SETTINGS['log_level']),
    format=LOG_SETTINGS['log_format'],
    datefmt=LOG_SETTINGS['date_format']
)


class ExcelAutomationService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ExcelAutomationService"
    _svc_display_name_ = "Excel Automation Service"
    _svc_description_ = "Service for automating Excel file updates"
    _svc_timeout_ = 20  # Timeout in seconds

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True
        logging.info("Service initialized")

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        try:
            logging.info("Service stop requested")
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.stop_event)
            self.is_alive = False
            logging.info("Service stopped successfully")
        except Exception as e:
            logging.error(f"Error stopping service: {str(e)}")
            raise

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        try:
            logging.info("Service starting...")
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )

            # Report that the service is running
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            logging.info("Service status set to RUNNING")

            # Run the main program
            main()

        except Exception as e:
            error_msg = f"Service failed: {str(e)}"
            logging.error(error_msg)
            servicemanager.LogErrorMsg(error_msg)
            self.SvcStop()
            raise


def door():
    if len(sys.argv) == 1:
        try:
            logging.info("Initializing service manager...")
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(ExcelAutomationService)
            logging.info("Starting service control dispatcher...")
            servicemanager.StartServiceCtrlDispatcher()
        except Exception as e:
            logging.error(f"Error in service initialization: {str(e)}")
            raise
    else:
        try:
            logging.info(f"Handling command line: {sys.argv[1]}")
            win32serviceutil.HandleCommandLine(ExcelAutomationService)
        except Exception as e:
            logging.error(f"Error handling command line: {str(e)}")
            raise


if __name__ == '__main__':
    door()