/********************************************************************************
 * Eclipse Tractus-X - Industry Core Hub Frontend
 *
 * Copyright (c) 2025 Contributors to the Eclipse Foundation
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Apache License, Version 2.0 which is available at
 * https://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the
 * License for the specific language govern in permissions and limitations
 * under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
********************************************************************************/


import { Grid2 } from '@mui/material';
import { PageNotifications } from '@catena-x/portal-shared-components';

interface PageNotificationProps {
  notification: { open: boolean; severity: "success" | "error"; title: string } | null;
}

const PageNotification = ({ notification }: PageNotificationProps) => {
  return (
    notification && (
      <Grid2 size={{xs: 12}}>
        <PageNotifications open severity={notification.severity} showIcon title={notification.title} />
      </Grid2>
    )
  );
};

export default PageNotification;
