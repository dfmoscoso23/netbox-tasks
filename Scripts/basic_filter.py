from extras.scripts import ChoiceVar, ObjectVar, Script
from dcim.models.racks import Rack
from dcim.choices import DeviceStatusChoices
from dcim.models.sites import Site
from dcim.models.devices import Device
from utilities.exceptions import AbortScript
from django.db.models import Q
import yaml

class DeviceQuery(Script):
    '''
    This script queries devices based on their status, site, and rack.
    It returns basic device data in YAML format.
    '''

    # Status is a required filter
    status = ChoiceVar(choices=DeviceStatusChoices)

    # Site and rack are optional filters
    site = ObjectVar(model=Site, required=False)
    rack = ObjectVar(model=Rack, required=False)

    def run(self, data, commit):
        """
        Executes the query based on the provided filters.
        Logs the number of devices found and outputs the results in YAML format.
        """
        site = data.get("site")
        rack = data.get("rack")
        
        #At least one filter more has to be selected
        if not site or rack:
            raise AbortScript("At least one filter more (site or rack) has to be selected")

        # The status filter is mandatory
        queries = [Q(status=data.get("status"))]

        # Apply the site filter if provided
        if site:
            queries.append(Q(rack__site__name=site))

        # Apply the rack filter if provided
        if rack:
            queries.append(Q(rack__name=rack))

        devices = Device.objects.filter(*queries)

        self.log_success(f"{devices.count()} Devices found")
        output = []
        for device in devices:
            self.log_info(message=f"Site {device.rack.site.name} ({device.rack.name}): #{device.id} - {device.name}", obj=device)

            # Format device details for output
            output.append({
            "name": device.name,
            "device_type": device.device_type.model,
            "role": device.role.name,
            "rack": device.rack.name,
            "position": f"U: {device.position}",
            "face": device.face,
            "status": device.get_status_display(),
            "site": device.rack.site.name
            })

        return yaml.dump({"devices":output}, default_flow_style=False, sort_keys=False)